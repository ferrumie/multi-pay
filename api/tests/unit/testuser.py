from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from api.tests.unit.base_test import BaseAPITestCase


class UserTestCase(BaseAPITestCase):
    client = APIClient()

    register_user_data = {

        "first_name": "Multi",
        "last_name": "pay",
        "email": "pay@pay.com",
        "phone_number": "+2348063133959",
        "password": "Testnig@18",
        "password2": "Testnig@18"

    }

    invalid_number_data = {
        "first_name": "Multi",
        "last_name": "pay",
        "email": "pay@pay.com",
        "phone_number": "+2349113133959",
        "password": "Testnig@18",
        "password2": "Testnig@18"
    }

    invalid_password_data = {

        "first_name": "Multi",
        "last_name": "pay",
        "email": "pay@pay.com",
        "phone_number": "+2348063133959",
        "password": "Testnig@18",
        "password2": "Testnigg@18"

    }

    create_api_key_data = {
        "api_key": "himTZj6xcFo4MvUd",
        "platform": "COINBASE"
    }

    create_duplicate_api_key_data = {
        "api_key": "erbefueubvueufryrbe",
        "platform": "COINBASE"
    }

    def test_user_token_create(self):
        # Create user
        response = self.client.post(
            reverse('register-user'), self.register_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_validate_phone_number(self):
        ''' Create user with invalid phone number (following google phonelib format)'''
        response = self.client.post(
            reverse('register-user'), self.invalid_number_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The phone number entered is not valid.',
                      response.data['phone_number'])

    def test_validate_password(self):
        ''' Create user with unmatching password number'''
        response = self.client.post(
            reverse('register-user'), self.invalid_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match',
                      str(response.data))

    def test_already_existing_mail(self):
        ''' You cant create different users with a single email'''
        response = self.client.post(
            reverse('register-user'), self.register_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create another user with same email
        response = self.client.post(
            reverse('register-user'), self.register_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user with this Email Address already exists.', response.data['email'])

    def test_add_api_key_for_payment_platform(self):
        # Create Api Key
        # Ensure that only authenticated user can do that
        response = self.client.post(
            reverse('apikeys'), self.create_api_key_data)

        # this should fail
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login and post again
        self.client.login(email='nobody@nobody.niks', password='nobody')
        response = self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_adding_api_key_for_existing_platform(self):
        '''
        You can not add multiple api key for a single platform
        Test for the error raised
        '''
        self.client.login(email='nobody@nobody.niks', password='nobody')
        response = self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # add same api key for another platform
        response = self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'You have already Added a Key for This platform')
