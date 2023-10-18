from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from gym import models
from datetime import time
GYM_URL = reverse('gym:gym-list')


def detail_url(id):
    '''Returns detail URL of a given object's id.'''
    return reverse('gym:gym-detail', args=[id])


def create_gym(user, **params):
    '''Create a gym objects.'''
    defaults = {
        'name': 'Test Gym',
        'number': '21312312',
        'address': 'Test address',
        'days_closed': 'Monday',
        'hour_open': '07:00:00',
        'hour_close': '22:00:00',
        'description': 'Test long description!',
    }
    defaults.update(params)
    gym = models.Gym.objects.create(owner=user, **defaults)

    return gym


class PublicApiTests(TestCase):
    '''Testing public API endpoints.'''
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            phone_number='111122331',
            password='testpass123'
        )

    def test_gym_list_success(self):
        '''Test listing gym endpoint.'''
        res = self.client.get(GYM_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_gym_retrieve_success(self):
        '''Test retrieving a gym object by its ID.'''
        gym = create_gym(self.user)  # Creating a gym object
        url = detail_url(id=gym.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateApiTests(TestCase):
    '''Test for Authentication-needed API endpoints.'''
    def setUp(self):
        self.client = APIClient()
        user_number = '2131231'
        self.user = get_user_model().objects.create_user(
            phone_number=user_number,
            password='testpass123',
            is_staff=True,
            is_superuser=True,  # Making the self.user admin and save it.
            is_active=True,
        )
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_create_gym(self):
        '''Test creating a gym object.'''
        payload = {
            'owner': self.user.id,  # string of ID because of nested data
            'name': 'New Gym',           # "social" field
            'number': '23154513',
            'address': 'Test address',
            'days_closed': 'Monday',
            'hour_open': '07:00:00',
            'hour_close': '22:00:00',
            'description': 'New long description!',
            'social': [
                {
                    'name': 'dev',
                    'link': 'http:/dev.com/'
                }
            ],
        }
        res = self.client.post(GYM_URL, payload, format='json')
        new_gym = models.Gym.objects.get(owner=self.user)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_gym.owner, self.user)

    def test_gym_partial_update(self):
        '''Test updating an existing gym instance.'''
        gym = create_gym(self.user)  # Create a gym instance.
        payload = {
            'name': 'Updated Gym',
            'number': '22334455',
            'address': 'Updated address',
            'days_closed': 'Updated Days',
            'description': 'Updated description!',
        }
        update_url = detail_url(gym.id)
        res = self.client.patch(update_url, payload)

        gym.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(gym.owner, self.user)

        for k, v in payload.items():
            self.assertEqual(getattr(gym, k), v)

    def test_gym_full_update(self):
        '''Test updating an existing gym instance.'''
        gym = create_gym(self.user)  # Create a gym instance.
        payload = {
            'name': 'Updated new Gym',
            'number': '2233445523',
            'address': 'Updated new address',
            'days_closed': 'Updated new Days',
            'description': 'Updated  newdescription!',
            'hour_open': time(8, 0, 0),
            'hour_close': time(23, 0, 0),
            'social': [
                {
                    'name': 'test',
                    'link:': 'link',
                }
            ]
        }
        update_url = detail_url(gym.id)
        res = self.client.put(update_url, payload)

        gym.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(gym.owner, self.user)

        if 'social' in payload.keys():
            payload.pop('social')
        for k, v in payload.items():
            self.assertEqual(getattr(gym, k), v)
