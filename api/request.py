import os
import json
import requests

from api.exceptions import ServiceUnavailable, UnauthorizedApiKey


class Request(object):
    """
    A custom request class that can be used by any of the payment API
    This provides some sort of uniformity and makes the api code cleaner
    """

    def __init__(self, base, api=None):
        self.api = api
        self.base = base
        self.path = None
        self.data = None
        self.res = None
        self.method = None

        # set headers
        self.headers = dict()

        if self.method != 'delete':
            self.headers['Content-Type'] = 'application/json'

        # create a send function that takes in the request

    def send(self):
        # set up the path,
        if self.api:
            self.path = os.path.join(self.base, self.api)
        else:
            self.path = self.base

        # set up data
        if self.data:
            self.data = json.dumps(self.data)

        # Set up request method
        # Using a dictionary instead of if-else
        # Uo make it less piled up and kind of mimic the switch case
        request_dict = {
            'get': requests.get,
            'put': requests.put,
            'patch': requests.patch,
            'post': requests.post,
            'delete': requests.delete
        }
        request_method = request_dict.get(self.method)
        try:
            self.res = request_method(
                self.path, headers=self.headers, 
                data=self.data, timeout=60)
        except requests.ConnectionError as e:
            raise ServiceUnavailable(str(e))
        except Exception as e:
            raise Exception(str(e))

        response = json.loads(self.res.content)
        content = response['message']
        if self.res.status_code == 401:
            raise UnauthorizedApiKey(content)
        if not 200 <= self.res.status_code < 300:
            raise Exception(str(content))
        else:
            return response
