from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
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

    def test_user_token_create(self):
        pass

    def test_validate_phone_number(self):
        pass

    def test_validate_password(self):
        pass

    def test_already_existing_mail(self):
        pass

    def test_add_api_key_for_payment_platform(self):
        pass

    def test_non_unique_api_key(self):
        pass

    def test_adding_api_key_for_existing_platform(self):
        '''
        You can not add multiple api key for a single platform
        Test for the error raised
        '''
        pass
