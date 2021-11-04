from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from api.tests.unit.base_test import BaseAPITestCase


class PaymentTestCase(BaseAPITestCase):
    client = APIClient()

    create_payment_data = {
        "amount": "1800.29",
        "title": "platform",
        "platform": "PAYSTACK"
    }

    create_api_key_data = {
        "api_key": "himTZj6xcFo4MvUd",
        "platform": "PAYSTACK"
    }

    create_payment_data_no_apikey = {
        "amount": "1800.29",
        "title": "platform",
        "platform": "STRIPE"
    }

    paystack_mock_data = {
        "link": "https://checkout.paystack.com/bprn7bz1jjyq8tu",
        "message": "Authorization URL created",
        "reference": "e7ca4da1-32e0-4f58-b9dd-45e28e8559f9"
    }
    paystack_verify_data = {
        "status": "success",
        "message": "Authorization URL created",
        "amount": "120"
    }

    paystack_verify_data_fail = {
        "status": "failed",
        "message": "Authorization URL Error",
        "amount": "120"
    }

    @patch('api.processor.PaymentProcessor.pay', return_value=paystack_mock_data)
    def test_make_payment_with_a_platform(self, mock_payment):
        ''' Make payment with a platform
            Return mocked data for easier test
        '''
        # Login and create api key for the platform
        self.client.login(email='nobody@nobody.niks', password='nobody')
        response = self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        response = self.client.post(
            reverse('payment'), self.create_payment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            'link', response.data)

    @patch('api.processor.PaymentProcessor.pay', return_value=paystack_mock_data)
    def test_make_payment_with_a_platform_with_no_api_key(self, mock_payment):
        '''
        Make payment with a platform without adding api key
        '''
        # Login
        self.client.login(email='nobody@nobody.niks', password='nobody')
        response = self.client.post(
            reverse('payment'), self.create_payment_data_no_apikey)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'You dont have an apikey for this platform', response.data['message'])

    @patch('api.processor.PaymentProcessor.pay', return_value=paystack_mock_data)
    @patch('api.processor.PaymentProcessor.verify', return_value=paystack_verify_data)
    def test_verify_payment_and_check_if_transaction_is_created(self, mock_payment, mock_verify):
        '''
        Verify payment through our redirect url
        '''

        # Add a payment first
        self.client.login(email='nobody@nobody.niks', password='nobody')
        self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        response = self.client.post(
            reverse('payment'), self.create_payment_data)

        # Now verify the payment
        # Get the payment transaction id
        verify_query_param = {
            'tx_ref': 'woi2h3i9ne93',
            'transaction_id': response.data['reference']
        }
        response.set_cookie('platform', ['PAYSTACK', 'paystack'])
        response = self.client.get(
            reverse('payment-confirm'), data=verify_query_param)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            'success', response.data['status'])

        # Check transaction List
        response = self.client.get(
            reverse('transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('api.processor.PaymentProcessor.pay', return_value=paystack_mock_data)
    @patch('api.processor.PaymentProcessor.verify', return_value=paystack_verify_data_fail)
    def test_verify_payment_when_failed(self, mock_payment, mock_verify):
        '''
        Verify payment through our redirect url
        '''

        # Add a payment first
        self.client.login(email='nobody@nobody.niks', password='nobody')
        self.client.post(
            reverse('apikeys'), self.create_api_key_data)
        response = self.client.post(
            reverse('payment'), self.create_payment_data)

        # Now verify the payment should fail
        # Get the payment transaction id
        verify_query_param = {
            'tx_ref': 'woi2h3i9ne93',
            'transaction_id': response.data['reference']
        }
        response = self.client.get(
            reverse('payment-confirm'), data=verify_query_param)
        self.assertTrue(mock_payment.is_called())
        self.assertTrue(mock_verify.is_called())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            'Authorization URL Error', response.data['message'])
