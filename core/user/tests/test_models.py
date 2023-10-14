from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTests(TestCase):
    '''
    Test Custom user manager.
    '''
    def test_create_user_success(self):
        '''Test creating a user successfully'''
        User = get_user_model()
        credentials = {
            'phone_number': '09129998877',
            'national_id': '3738882164',
            'name': 'Test Name',
            'password': 'testpass123',

        }
        user = User.objects.create_user(**credentials)

        for k, v in credentials.items():
            if k != 'password':
                self.assertEqual(getattr(user, k), v)
        self.assertTrue(user.check_password(credentials['password']))
        self.assertEqual(str(user), credentials['name'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_coach)

    def test_create_superuser_success(self):
        '''Test creating superuser successfully.'''
        User = get_user_model()
        credentials = {
            'phone_number': '09129992211',
            'national_id': '3738883366',
            'name': 'Test Name',
            'password': 'testpass123',
        }
        admin = User.objects.create_superuser(**credentials)

        for k, v in credentials.items():
            if k != 'password':
                self.assertEqual(getattr(admin, k), v)
        self.assertTrue(admin.check_password(credentials['password']))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_coach)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                **credentials,
                is_staff=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                **credentials,
                is_superuser=False
            )
