from api.extenal.ravepayment import RavePayment
from api.payment import PaymentMethodFactory


payment_methods = PaymentMethodFactory()
payment_methods.register_payment_method('rave_payment', RavePayment)


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
