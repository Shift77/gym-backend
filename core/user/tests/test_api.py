from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import PendingUser, User

class UserApiTests(TestCase):
    '''
    Test user API endpoints.
    '''
    def setUp(self) -> None:
        self.create_url = reverse('user:create-user')
        self.client  = APIClient()

    def test_duplicate_phone_number_error(self):
        '''Test duplicate phone number cant register.'''
        user = User.objects.create_user(
            phone_number='1111',
            password='testpass123',
            national_id='231233',
            name='Test User'
        )
        payload = {
            'phone_number': '1111',  # Same phone number as the user.
            'password': 'testpass123',
            'national_id': '23145453',
            'name': 'New User',
        }
        res = self.client.post(self.create_url, payload)

        self.assertEqual(res.status_code, 400)
