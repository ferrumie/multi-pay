import os
from api.exceptions import StripeException

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction


class StripePayment(Request, PaymentInterface):
    def __init__(self):
        url = os.getenv("STRIPE_API_URL")
        super(StripePayment, self).__init__(base=url)
        print(url)
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def pay(self, payload):
        user = payload.get("user")
        amount = payload.get("amount")
        title = payload.get("title")
        logo = payload.get('logo')
        description = payload.get("description")
        redirect_url = payload.get("redirect_url")
        currency = payload.get('currency')
        api_key = payload.get('api_key')

        payload = {
            "mode": "payment",
            "line_items": [
                {
                    "amount": str(amount),
                    "currency": currency,
                    "name": title,
                    "description": description
                }
            ],
            "payment_method_types": ["card"],
            "success_url": redirect_url,
            "cancel_url": 'api/',
            "metadata": {
                "customer_name": f'{user.first_name} {user.last_name}',
                "customer_id": user.id
            },
        }
        self.method = 'post'
        self.api = 'sessions'
        self.headers['Authorization'] = f'Bearer {api_key}'
        self.data = payload
        response = dict()
        response = super(StripePayment, self).send()
        breakpoint()
        res = {
            "hosted_url": response['data']['hosted_url'],
            "status": response['status'],
            "code": response['data']['code'],
            "created_at": response['data']['created_at'],
            "expires_at": response['data']['expires_at']
        }
        return res

    def verify(self, payload):
        user = payload.get("user")
        api_key = payload.get('api_key')
        transaction_id = payload.get("transaction_id")
        method = payload.get("method")
        self.method = 'get'
        self.api = f'{transaction_id}'
        self.headers['Authorization'] = f'Bearer {api_key}'
        response = dict()
        try:
            if transaction_id:
                response = super(StripePayment, self).send()
                tran = Transaction.objects.filter(
                    user=user).filter(transaction_id=transaction_id)
                if not tran:
                    transaction = {
                        'amount': response['pricing']['local']['amount'],
                        'transaction_id': transaction_id,
                        'transaction_ref': response['data']['id'],
                        'platform': method,
                        'user': user,
                        'status': response['status'],
                        'payment_type': response['pricing_type']
                    }
                    transact = Transaction.objects.create(**transaction)
                    transact.save()

                return response
            raise ValueError({"message": "Transaction id is required"})
        except Exception as e:
            raise StripeException(str(e))
