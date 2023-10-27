from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from plan.models import Plan, SubPlan, Exercise

PLAN_LIST = reverse('plan:plan-list')


def create_plan_detail_url(id):
    return reverse('plan:plan-detail', args=[id])


def create_exercise(created_by):
    '''Create exercise objects.'''
    exercise = Exercise.objects.create(
        created_by=created_by,
        name='Test Exercise',
        main_target_muscle='Test muscle',
        secondary_target_muscle='Second muscle',
        rep_range='6-10',
        number_of_sets=4,
        description="test description."
    )
    return exercise


class PrivatePlanApiTests(TestCase):
    '''Test for Plan endpoints that require authentication.'''
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
        self.normal_user = get_user_model().objects.create_user(
            phone_number='289883123',
            password='testpass123',
            is_coach=False,
            is_staff=False,
        )
        self.normal_client = APIClient()
        self.normal_client.force_authenticate(user=self.normal_user)
        self.only_coach_user = get_user_model().objects.create_user(
            phone_number='28912123123',
            password='testpass123',
            is_coach=True,
            is_staff=False,
        )
        self.only_coach_client = APIClient()
        self.only_coach_client.force_authenticate(user=self.only_coach_user)

    def test_list_plan_success(self):
        '''Test for listing plans.'''
        plan = Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        sub_plan = SubPlan.objects.create(
            plan=plan,
            name='Sub Plan',
            week_number=1,
            day_number=1,
            description='Description!',
        )
        exercise = Exercise.objects.create(
            created_by=self.only_coach_user,
            name='Tes Name',
            main_target_muscle='Test muscle',
            secondary_target_muscle='Second Muscle',
            number_of_sets=3,
            rep_range='12-15',
            description='Test Description!'
        )
        sub_plan.exercises.set([exercise])
        res = self.only_coach_client.get(PLAN_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_plan_fail(self):
        '''Test for listing plans fail.'''
        Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        res = self.normal_client.get(PLAN_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_plan_success(self):
        '''Test retrieving a plan successfully.'''
        plan = Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        url = create_plan_detail_url(plan.id)
        res = self.only_coach_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_plan_fail(self):
        '''Test retrieving a plan fail.'''
        plan = Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        url = create_plan_detail_url(plan.id)
        res = self.normal_client.get(url)
        res_2 = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_plan_success(self):
        '''Test deleting a plan successfully.'''
        plan = Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        url = create_plan_detail_url(plan.id)
        res = self.only_coach_client.delete(url)  # THe creator of instance.

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Plan.objects.filter(id=plan.id).exists())

    def test_delete_plan_fail(self):
        '''Test deleting a plan fail.'''
        plan = Plan.objects.create(
            coach=self.only_coach_user,
            target_user=self.normal_user,
            name='test name',
            gender='no difference',
            description='Test description'
        )
        url = create_plan_detail_url(plan.id)
        # self.normal_client is neither the creator of the instance
        # nor an admin to be able to delete the record.
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Plan.objects.filter(id=plan.id).exists())
