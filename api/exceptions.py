from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class UnauthorizedApiKey(APIException):
    status_code = 401
    default_detail = 'Your Api key is not correct.'
    default_code = 'incorrect_api_key'


class FlutterException(APIException):
    status_code = 400
    default_detail = 'Error Returned from Rave api'
