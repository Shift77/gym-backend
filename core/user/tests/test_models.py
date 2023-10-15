from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    '''Test cases for models.'''
    def test_create_user(self):
        '''Test creating a user.'''
        User = get_user_model()
        payload = {
            'phone_number': '09129998877',
            'password': 'testpass123',
            'national_id': '23165468',
            'name': 'Test Name'
        }
        user = User.objects.create_user(**payload)

        for k, v in payload.items():
            if k != 'password':
                self.assertEqual(getattr(user, k), v)
        self.assertTrue(user.check_password(payload['password']))
        with self.assertRaises(ValueError):
            User.objects.create_user(phone_number='', password='testpass')
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(phone_number='')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_coach)

    def test_create_super_user(self):
        '''Test Creating Superuser.'''
        User = get_user_model()
        admin = User.objects.create_superuser(
            phone_number='09128889922',
            password='testpass123'
        )
        self.assertEqual(admin.phone_number, '09128889922')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_coach)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone_number='09128889922',
                password='testpass123',
                is_staff=True,
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone_number='09128889922',
                password='testpass123',
                is_staff=False,
                is_superuser=False,
            )
