import os
from api.exceptions import StripeException

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction


class CoinBasePayment(Request, PaymentInterface):
    def __init__(self):
        url = os.getenv("COINBASE_API_URL")
        super(CoinBasePayment, self).__init__(base=url)

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
            "pricing_type": "fixed_price",
            "local_price": {
                "amount": str(amount),
                "currency": currency,
            },
            "redirect_url": redirect_url,
            "metadata": {
                "customer_name": f'{user.first_name} {user.last_name}',
                "customer_id": user.id
            },
            "name": title,
            "logo": logo,
            "description": description

        }
        self.method = 'post'
        self.api = 'payments'
        self.headers['Authorization'] = f'Bearer {api_key}'
        self.data = payload
        response = dict()
        response = super(CoinBasePayment, self).send()
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
                response = super(CoinBasePayment, self).send()
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
