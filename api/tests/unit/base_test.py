from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


User = get_user_model()


class BaseAPITestCase(APITestCase):

    """
    Base setup to create different test cases for cleaner code
    """
    client = APIClient

    def setUp(self):

        user = User.objects.create_user(
            email="nobody@nobody.niks", password="nobody"
        )
        user.is_staff = False
        user.is_superuser = False
        user.role = 'USER'
        user.save()

        user = User.objects.create_user(
            email="somebody@nobody.niks", password="somebody"
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()

    def tearDown(self):
        User.objects.filter(email="nobody@nobody.niks").delete()
        User.objects.filter(email="somebody@nobody.niks").delete()
