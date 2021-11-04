from api.extenal.coinbase import CoinBasePayment
from api.extenal.paystack import PayStackPayment
from api.extenal.ravepayment import RavePayment
from api.extenal.sripe import StripePayment
from api.payment import PaymentMethodFactory


payment_methods = PaymentMethodFactory()
payment_methods.register_payment_method('rave_payment', RavePayment)
payment_methods.register_payment_method('paystack', PayStackPayment)
payment_methods.register_payment_method('coinbase', CoinBasePayment)
payment_methods.register_payment_method('stripe', StripePayment)


class PaymentProcessor:
    '''
    This processes the method gotten from the payment method factory
    It is called by the views,
    Gets the payment method, (say, paystack) from payment method factory
    then get the class responsible to the payment processing of that method
    and calls either the pay or verify method
    '''
    @classmethod
    def pay(cls, method, **kwargs):
        ''' Calls the pay method of the payment class'''
        payment_method = payment_methods.select_payment_method(method)
        payload = kwargs
        return payment_method().pay(payload)

    @classmethod
    def verify(cls, method, **kwargs):
        ''' Calls the verify method f the payment class'''
        payment_method = payment_methods.select_payment_method(method)
        kwargs['method'] = method
        payload = kwargs
        return payment_method().verify(payload)
