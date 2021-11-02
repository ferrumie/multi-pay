from api.extenal.coinbase import CoinBasePayment
from api.extenal.paystack import PayStackPayment
from api.extenal.ravepayment import RavePayment
from api.extenal.sripe import StripePayment
from api.payment import PaymentMethodFactory


payment_methods = PaymentMethodFactory()
payment_methods.register_payment_method('rave_payment', RavePayment)
payment_methods.register_payment_method('paystack', PayStackPayment)
payment_methods.register_payment_method('paystack', CoinBasePayment)
payment_methods.register_payment_method('paystack', StripePayment)


class PaymentProcessor:
    @classmethod
    def pay(cls, method, **kwargs):
        payment_method = payment_methods.select_payment_method(method)
        payload = kwargs
        return payment_method().pay(payload)

    @classmethod
    def verify(cls, method, **kwargs):
        payment_method = payment_methods.select_payment_method(method)
        kwargs['method'] = method
        payload = kwargs
        return payment_method().verify(payload)
