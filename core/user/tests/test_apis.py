from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

CREATE_URL = reverse('user:create')
OBTAIN_TOKEN_URL = reverse('obtain-token')
REFRESH_TOKEN_URL = reverse('refresh-token')
PROFILE_URL = reverse('user:profile')


class PublicApiTests(TestCase):
    '''Test public API endpoints.'''
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''Test creating a user successfully.'''
        User = get_user_model()
        payload = {
            'phone_number': '09129987722',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_URL, payload)
        user = User.objects.get(phone_number=payload['phone_number'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.phone_number, payload['phone_number'])
        self.assertNotIn('password', res.data)

    def test_create_user_bad_credentials_error(self):
        '''Test Creating a user with bad credentials.'''
        res = self.client.post(CREATE_URL, {
            'phone_number': '',
            'password': ''
        })
        res_1 = self.client.post(CREATE_URL, {
            'phone_number': '',
            'password': 'testpass123'
        })
        res_2 = self.client.post(CREATE_URL, {
            'phone_number': '56419888',
            'password': ''
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_exists_error(self):
        '''Getting error user exists.'''
        User = get_user_model()
        phone_num = '09128887766'
        User.objects.create_user(
            phone_number=phone_num,
            password='testpass123'
        )
        payload = {
            'phone_number': phone_num,
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_jwt_token(self):
        '''Test obtaining a jwt token for registered users. '''
        payload = {
            'phone_number': '09127772233',
            'password': 'testpass123',
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(OBTAIN_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_jwt_token(self):
        '''Test refreshing jwt token of a user.'''
        payload = {
            'phone_number': '0912773293',
            'password': 'testpass123',
        }
        get_user_model().objects.create_user(**payload)
        obtain_token = self.client.post(OBTAIN_TOKEN_URL, payload)

        res = self.client.post(REFRESH_TOKEN_URL, {
            'refresh': obtain_token.data['refresh']
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateApiTests(TestCase):
    '''Test authentication required API endpoints.'''
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            phone_number='2222',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)

    def test_get_user_profile(self):
        '''Test getting the user profile.'''
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['phone_number'], '2222')

    def test_update_user_profile(self):
        '''Test updating user profile.'''
        user = get_user_model().objects.get(phone_number='2222')
        payload = {
            'phone_number': '3333',
            'password': 'updatedpass',
            'name': 'updated name',
            'national_id': '12345678'
        }
        res = self.client.put(PROFILE_URL, payload)
        user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for k, v in payload.items():
            if k != 'password':
                self.assertEqual(getattr(user, k), v)
        self.assertTrue(user.check_password(payload['password']))
