
from abc import ABC, abstractmethod


class PaymentMethodFactory:
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
    "defines behaviour of all payment interface"

    @abstractmethod
    def pay(self, payload):
        pass

    @abstractmethod
    def verify(self, payload):
        pass
