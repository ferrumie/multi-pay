

class PaymentMethodFactory:
    def __init__(self):
        self.payment_methods = {}

    def register_payment_method(self, method, processor):
        self.payment_methods[method] = processor

    def select_payment_method(self, method):
        try:
            