from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from plan import models


EXERCISE_LIST = reverse('plan:exercise-list')
def create_exercise_detail_url(id):
    return reverse('plan:exercise-detail', args=[id])


class PrivateExerciseApiTests(TestCase):
    '''Test for Exercise endpoints that require authentication.'''
    def setUp(self):
        '''Creating Three different users with three different permissions.'''
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            phone_number='23123123',
            password='testpass123',
            is_coach=True,
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        not_coach = get_user_model().objects.create_user(
            phone_number='289883123',
            password='testpass123',
            is_coach=False,
            is_staff=False,
        )
        self.normal_client = APIClient()
        self.normal_client.force_authenticate(user=not_coach)
        self.only_coach_user = get_user_model().objects.create_user(
            phone_number='28912123123',
            password='testpass123',
            is_coach=True,
            is_staff=False,
        )
        self.only_coach_client = APIClient()
        self.only_coach_client.force_authenticate(user=self.only_coach_user)
    def test_get_exercise_success(self):
        '''Test creating a plan.'''
        res = self.client.get(EXERCISE_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_exercise_success(self):
        '''Test creating an exercise.'''
        payload = {
            'name': 'super name',
            'main_target_muscle': 'Lats',
            'secondary_target_muscle': 'Biceps',
            'description': 'TEst desc!',
            'rep_range': '8-12',
            'number_of_sets': 4,
        }
        res = self.client.post(EXERCISE_LIST, payload)
        e = models.Exercise.objects.get(name=payload['name'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            models.Exercise.objects.filter(name=payload['name']).exists()
            )
        self.assertEqual(e.created_by, self.user)

    def test_get_detail_exercise_success(self):
        '''Test getting a details of an exercise by id.'''
        exercise = models.Exercise.objects.create(
            created_by=self.user,
            name='Test Exercise',
            main_target_muscle='Test body part',
            secondary_target_muscle='second body part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        url = create_exercise_detail_url(exercise.id)
        res = self.normal_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise.created_by, self.user)

    def test_create_exercise_fail(self):
        '''Test creating an exercise with a non coach user fail.'''
        payload = {
            'name': 'Test Name',
            'main_target_muscle': 'Arms',
            'secondary_target_muscle': 'Back',
            'description': 'TEst desc!',
            'rep_range': '8-12',
            'number_of_sets': 4,
        }
        #  Self.normal_client is neither coach nor is_staff.
        res = self.normal_client.post(EXERCISE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_exercise_success(self):
        '''Test deleting an exercise object successfully.'''
        exercise = models.Exercise.objects.create(
            created_by=self.user,
            name='Test 2',
            main_target_muscle='Test body 2 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        url = create_exercise_detail_url(exercise.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            models.Exercise.objects.filter(name='Test 2').exists()
            )
    def test_destroy_exercise_fail(self):
        '''Test deleting an exercise object fail.'''
        exercise = models.Exercise.objects.create(
            created_by=self.user,
            name='Test 243',
            main_target_muscle='Test body 123 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        url = create_exercise_detail_url(exercise.id)
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(  # The objects should still exist.
            models.Exercise.objects.filter(name='Test 243').exists()
            )

    def test_update_exercise_success(self):
        '''Test updating the exercise successfully.'''
        exercise = models.Exercise.objects.create(
            created_by=self.only_coach_user,
            name='Test 0987',
            main_target_muscle='Test body 123 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        payload = {
            'name': 'Test Name',
            'main_target_muscle': 'Arms',
            'secondary_target_muscle': 'Back',
            'description': 'TEst desc!',
            'rep_range': '8-12',
            'number_of_sets': 4,
        }
        url = create_exercise_detail_url(exercise.id)
        res = self.only_coach_client.put(url, payload)
        exercise.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for k, v in payload.items():
            self.assertEqual(getattr(exercise, k), v)

    def test_update_exercise_fail(self):
        '''Test updating the exercise fail.'''
        exercise = models.Exercise.objects.create(
            created_by=self.only_coach_user,
            name='Test 0987',
            main_target_muscle='Test body 123 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        payload = {
            'name': 'Test Name',
            'main_target_muscle': 'Arms',
            'secondary_target_muscle': 'Back',
            'description': 'TEst desc!',
            'rep_range': '5-8',
            'number_of_sets': 4,
        }
        url = create_exercise_detail_url(exercise.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        for k, v in payload.items():
            self.assertNotEqual(getattr(exercise, k), v)

    def test_partial_update_exercise_success(self):
        '''Test partial updating the exercise successfully.'''
        exercise = models.Exercise.objects.create(
            created_by=self.only_coach_user,
            name='Test 0987',
            main_target_muscle='Test body 123 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        payload = {
            "name": "Test name u",
            }
        url = create_exercise_detail_url(exercise.id)
        res = self.only_coach_client.patch(url, payload)
        exercise.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise.name, payload['name'])

    def test_partial_update_exercise_fail(self):
        '''Test partial updating the exercise fail.'''
        exercise = models.Exercise.objects.create(
            created_by=self.only_coach_user,
            name='Test 0987',
            main_target_muscle='Test body 123 part',
            secondary_target_muscle='second body 3 part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )
        payload = {
            'name': 'Test Name',
            'main_target_muscle': 'Arms',
            'number_of_sets': 5,
        }
        url = create_exercise_detail_url(exercise.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        for k, v in payload.items():
            self.assertNotEqual(getattr(exercise, k), v)
