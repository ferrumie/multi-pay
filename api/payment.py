
from abc import ABC, abstractmethod


class PaymentMethodFactory:
    '''
    This 'cooks' the payment methods
    Gets the method and the processor class
    and returns the preferred payment method

    -> register a method by providing the method the its payment class
    -> it the method gets mapped to the class, and the class is returned
    eg payment_methods.register_payment_method('rave_payment', RavePayment)
    '''

    def __init__(self):
        self.payment_methods = {}

    def register_payment_method(self, method, processor):
        self.payment_methods[method] = processor

    def select_payment_method(self, method):
        preferred_payment_method = self.payment_methods.get(method.lower())
        if preferred_payment_method is None:
            return ValueError(method)
        return preferred_payment_method


class PaymentInterface(ABC):
    '''
    Abstract Skeleton class for the payment class
    '''

    @abstractmethod
    def pay(self, payload):
        pass

    @abstractmethod
    def verify(self, payload):
        pass
