import os
import stripe
from api.exceptions import FlutterException

from api.payment import PaymentInterface
from api.request import Request
from transaction.models import Transaction


class SripePayment(Request, PaymentInterface):

    def pay(self, payload):
        user = payload.get("user")
        tx_ref = payload.get("tx_ref")
        amount = payload.get("amount")
        description = payload.get("description")
        redirect_url = payload.get("redirect_url")
        currency = payload.get('currency')
        api_key = payload.get('api_key')
