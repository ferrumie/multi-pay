import os

from api.payment import PaymentInterface, PaymentMethodFactory
from api.request import Request


class RavePayment(Request, PaymentInterface):
    def __init__(self):
        url = os.getenv("FLUTTERWAVE_API_URL")
        super(RavePayment, self).__init__(base=url)

    def pay(self, payload):
        user = payload.get("user")
        guest_email = payload.get("guest_email")
        anon_user = user.is_anonymous
        tx_ref = payload.get("tx_ref")
        amount = payload.get("amount")
        title = payload.get("title")
        logo = payload.get('logo')
        description = payload.get("description")
        redirect_url = payload.get("redirect_url")
        currency = settings.OSCAR_DEFAULT_CURRENCY
        payload = {
            "user_id": user.id,
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "meta": {
                "user_id": user.id,
                "plan_id": plan_id
            },
            "payment_options": "card, account, banktransfer, ussd, barter, credit, payattitude, paga",
            "redirect_url": redirect_url,
            "customer": {
                "name": f'{user.first_name} {user.last_name}' if not anon_user else 'ANON',
                "email": user.email if not anon_user else guest_email
            },
            "customizations": {
                "title": title,
                "logo": logo,
                "description": description
            }
        }
        self.method = 'post'
        self.api = 'payments'
        self.headers['Authorization'] = f'Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}'
        self.data = payload
        response = dict()
        response = super(RavePayment, self).send()
        res = {
            "link": response['data']['link'],
            "status": response['status']
        }
        return res

    def verify(self, payload):
        transaction_id = payload.get("transaction_id")
        tx_ref = payload.get("tx_ref")
        self.method = 'get'
        self.api = f'transactions/{transaction_id}/verify'
        self.headers['Authorization'] = f'Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}'
        response = dict()
        try:
            if transaction_id:
                response = super(RavePayment, self).send()
                if (response.get('status') == 'success') and \
                        (response['data'].get('tx_ref') == tx_ref):
                    return response
                return {'message': False}
            raise ValueError({"message": "Transaction id is required"})
        except Exception as e:
            raise Exception(str(e))


payment_methods = PaymentMethodFactory()
payment_methods.register_payment_method('rave_payment', RavePayment)
