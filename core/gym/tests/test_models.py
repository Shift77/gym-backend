from django.test import TestCase
from django.contrib.auth import get_user_model
from gym import models
from datetime import time


class ModelTests(TestCase):
    '''Test models.'''
    def test_create_gym_model(self):
        '''Test creating a gym instance.'''
        owner = get_user_model().objects.create_user(
            phone_number='112233',
            password='tespass123',
            )
        payload = {
            'name': 'Test Gym',
            'number': '231231',
            'address': 'Sanandaj-Azadi square',
            'owner': owner,
            'days_closed': 'Friday',
            'hour_open': time(8, 0, 0),
            'hour_close': time(22, 0, 0),
            'description': 'Description for gym!',
        }
        gym = models.Gym.objects.create(**payload)

        for k, v in payload.items():
            self.assertEqual(getattr(gym, k), v)

    def test_create_review_model(self):
        '''Test creating a review instance.'''
        user = get_user_model().objects.create_user(
            phone_number='112233',
            password='tespass123',
            )
        owner = get_user_model().objects.create_user(
            phone_number='11232233',
            password='tespass123',
            )
        gym_payload = {
            'name': 'Test Gym',
            'number': '231231',
            'address': 'Sanandaj-Azadi square',
            'owner': owner,
            'days_closed': 'Friday',
            'hour_open': time(8, 0, 0),
            'hour_close': time(22, 0, 0),
            'description': 'Description for gym!',
        }
        gym = models.Gym.objects.create(**gym_payload)

        payload = {
            'gym': gym,
            'name': 'Review Test',
            'author': user,
            'description': 'My review of the gym.'

        }
        review = models.Review.objects.create(**payload)

        for k, v in payload.items():
            self.assertEqual(getattr(review, k), v)

    def test_create_social_model(self):
        '''Test creating a social instance.'''
        owner = get_user_model().objects.create_user(
            phone_number='112233',
            password='tespass123',
            )
        gym_payload = {
            'name': 'Test Gym',
            'number': '231231',
            'address': 'Sanandaj-Azadi square',
            'owner': owner,
            'days_closed': 'Friday',
            'hour_open': time(8, 0, 0),
            'hour_close': time(22, 0, 0),
            'description': 'Description for gym!',
        }
        gym = models.Gym.objects.create(**gym_payload)

        payload = {
            'gym': gym,
            'name': 'Youtube',
            'link': 'http://youtube.com/',
        }
        link = models.Social.objects.create(**payload)

        for k, v in payload.items():
            self.assertEqual(getattr(link, k), v)
