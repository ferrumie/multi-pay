import os

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction


class CoinBasePayment(Request, PaymentInterface):
    def __init__(self):
        url = os.getenv("COINBASE_API_URL")
        super(CoinBasePayment, self).__init__(base=url)

    def pay(self, payload):
        user = payload.get("user")
        tx_ref = payload.get("tx_ref")
        amount = payload.get("amount")
        redirect_url = payload.get("redirect_url")
        currency = payload.get('currency')
        api_key = payload.get('api_key')
        payload = {
            "user_id": user.id,
            "reference": tx_ref,
            "amount": str(amount),
            "currency": currency,
            "meta": {
                "user_id": user.id
            },
            "payment_options": "card, account, banktransfer, ussd, barter, credit, payattitude, paga",
            "callback_url": redirect_url,
            "email": user.email,
            "metadata": {
                "user": user.id,
            }
        }
        self.method = 'post'
        self.api = 'initialize'
        self.headers['Authorization'] = f'Bearer {api_key}'
        self.data = payload
        response = dict()
        response = super(PayStackPayment, self).send()
        link = response['data']['authorization_url']
        reference = response['data']['reference']
        res = {
            "link": link,
            "message": response['message'],
            "reference": reference
        }
        return res

    def verify(self, payload):
        user = payload.get("user")
        api_key = payload.get('api_key')
        transaction_id = payload.get("transaction_id")
        method = payload.get("method")
        self.method = 'get'
        self.api = f'verify/{transaction_id}'
        self.headers['Authorization'] = f'Bearer {api_key}'
        response = dict()
        try:
            if transaction_id:
                response = super(PayStackPayment, self).send()
                tran = Transaction.objects.filter(
                    user=user).filter(transaction_id=transaction_id)
                if not tran:
                    transaction = {
                        'amount': response['data']['amount'],
                        'transaction_id': transaction_id,
                        'transaction_ref': response['data']['reference'],
                        'platform': method,
                        'user': user,
                        'status': response['status'],
                        'payment_type': response['data']['authorization']['card_type']
                    }
                    transact = Transaction.objects.create(**transaction)
                    transact.save()

                return response
            raise ValueError({"message": "Transaction id is required"})
        except Exception as e:
            raise PaystackException(str(e))
