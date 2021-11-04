from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class UnauthorizedApiKey(APIException):
    '''
    Custom exception if api key is not correct
    '''
    status_code = 401
    default_detail = 'Your Api key is not correct.'
    default_code = 'incorrect_api_key'


class FlutterException(APIException):
    ''' Catch Generic Exceptions from flutterwave'''
    status_code = 400
    default_detail = 'Error Returned from Rave api'


class PaystackException(APIException):
    ''' Catch Generic Exceptions from paystack'''
    status_code = 400
    default_detail = 'Error Returned from Paystackapi'


class CoinBaseException(APIException):
    ''' Catch Generic Exceptions from coinbase'''
    status_code = 400
    default_detail = 'Error Returned from CoinBaseApi'


class StripeException(APIException):
    ''' Catch Generic Exceptions from stripe'''
    status_code = 400
    default_detail = 'Error Returned from StripeApi'
