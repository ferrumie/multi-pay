import os
from api.exceptions import StripeException

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction
import stripe


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
        amount = int(round(amount*100))

        stripe.api_key = api_key
        response = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email=user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'product_data': {
                            'name': title,
                            'logo': logo,
                            'description': description
                        },
                        'currency': currency,
                        'unit_amount': str(amount),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=redirect_url,
            cancel_url=f'{redirect_url}/cancel',
        )

        res = {
            "hosted_url": response.url,
            "code": response.id,
            "expires_at": response.expires_at
        }
        return res

    def verify(self, payload):
        user = payload.get("user")
        api_key = payload.get('api_key')
        transaction_id = payload.get("transaction_id")
        method = payload.get("method")
        stripe.api_key = api_key
        response = stripe.checkout.Session.retrieve(transaction_id)
        try:
            if transaction_id:
                response = super(StripePayment, self).send()
                tran = Transaction.objects.filter(
                    user=user).filter(transaction_id=transaction_id)
                if not tran:
                    transaction = {
                        'amount': response.amount_total,
                        'transaction_id': transaction_id,
                        'transaction_ref': response.id,
                        'platform': method,
                        'user': user,
                        'status': response.payment_status,
                        'payment_type': response.method
                    }
                    transact = Transaction.objects.create(**transaction)
                    transact.save()

                return response
            raise ValueError({"message": "Transaction id is required"})
        except Exception as e:
            raise StripeException(str(e))
