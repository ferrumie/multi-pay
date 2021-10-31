import os
from api.exceptions import FlutterException

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction


class RavePayment(Request, PaymentInterface):
    def __init__(self):
        url = os.getenv("FLUTTERWAVE_API_URL")
        super(RavePayment, self).__init__(base=url)

    def pay(self, payload):
        user = payload.get("user")
        tx_ref = payload.get("tx_ref")
        amount = payload.get("amount")
        title = payload.get("title")
        logo = payload.get('logo')
        description = payload.get("description")
        redirect_url = payload.get("redirect_url")
        currency = payload.get('currency')
        api_key = payload.get('api_key')
        print(redirect_url)
        payload = {
            "user_id": user.id,
            "tx_ref": tx_ref,
            "amount": str(amount),
            "currency": currency,
            "meta": {
                "user_id": user.id
            },
            "payment_options": "card, account, banktransfer, ussd, barter, credit, payattitude, paga",
            "redirect_url": redirect_url,
            "customer": {
                "name": f'{user.first_name} {user.last_name}',
                "email": user.email
            },
            "customizations": {
                "title": title,
                "logo": logo,
                "description": description
            }
        }
        self.method = 'post'
        self.api = 'payments'
        self.headers['Authorization'] = f'Bearer {api_key}'
        self.data = payload
        response = dict()
        response = super(RavePayment, self).send()
        # Extracting Transaction id from the link
        link = response['data']['link']
        link_list = link.split('/')
        transaction_id = link_list[-1]
        res = {
            "link": response['data']['link'],
            "status": response['status'],
            "transaction_id": transaction_id
        }
        return res

    def verify(self, payload):
        user = payload.get("user")
        api_key = payload.get('api_key')
        transaction_id = payload.get("transaction_id")
        transaction_ref = payload.get("tx_ref")
        method = payload.get("method")
        self.method = 'get'
        self.api = f'transactions/{transaction_id}/verify'
        self.headers['Authorization'] = f'Bearer {api_key}'
        response = dict()
        try:
            if transaction_id:
                response = super(RavePayment, self).send()
                tran = Transaction.objects.filter(user=user).filter(transaction_id=transaction_id)
                if not tran:
                    transaction = {
                        'amount': response['data']['amount'],
                        'transaction_id': transaction_id,
                        'transaction_ref': transaction_ref,
                        'platform': method,
                        'user': user,
                        'status': response['status'],
                        'payment_type': response['data']['payment_type'],
                        'account_id': response['data']['account_id']
                    }
                    transact = Transaction.objects.create(**transaction)
                    transact.save()

                return response
            raise ValueError({"message": "Transaction id is required"})
        except Exception as e:
            raise FlutterException(str(e))
