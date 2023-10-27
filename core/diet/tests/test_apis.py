from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from diet.models import Diet, Routine

# FOOD_URL = reverse('diet:food-list')
DIET_URL = reverse('diet:diet-list')

# def create_food_detail_url(id):
#     '''Create a food detail url.'''
#     return reverse('diet:food-detail', args=[id])


def create_diet_detail_url(id):
    return reverse('diet:diet-detail', args=[id])


class PrivateApiTests(TestCase):
    '''Test private api endpoints that need authentication.'''
    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            phone_number='23123123',
            password='testpass123'
        )
        self.coach_user = get_user_model().objects.create_user(
            phone_number='231231265673',
            password='testpass123',
            is_coach=True
        )
        self.normal_user = get_user_model().objects.create_user(
            phone_number='2389723',
            password='testpass123'
        )
        self.coach_user_2 = get_user_model().objects.create_user(
            phone_number='28889931265673',
            password='testpass123',
            is_coach=True
        )
        self.super_client = APIClient()
        self.super_client.force_authenticate(
            user=self.super_user
            )
        self.coach_client = APIClient()
        self.coach_client.force_authenticate(
            user=self.coach_user
            )
        self.coach_client_2 = APIClient()
        self.coach_client_2.force_authenticate(
            user=self.coach_user_2
            )
        self.normal_client = APIClient()
        self.normal_client.force_authenticate(
            user=self.normal_user
            )

    # def test_get_list_food_success(self):
    #     '''Test getting all user's created foods.'''
    #     res = self.coach_client.get(FOOD_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_get_list_food_permission_fail(self):
    #     '''Test getting all user's created foods fail for permission.'''
    #     # Self.normal_client is not a coach and must not access the URL.
    #     res = self.normal_client.get(FOOD_URL)

    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_food_success(self):
    #     '''Test creating a food instance.'''
    #     payload = {
    #         'name': 'Test food123',
    #         'quantity_in_grams': 100,
    #         'protein': Decimal('24.2'),
    #         'fat': Decimal('13.5'),
    #         'carb': Decimal('6.2'),
    #         'calories': Decimal('126.68'),
    #     }
    #     res = self.coach_client.post(FOOD_URL, payload)
    #     obj = Food.objects.get(name=payload['name'])

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(obj.created_by, self.coach_user)

    # def test_full_update_food_success(self):
    #     '''Test updating a food successfully.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test food123',
    #         quantity_in_grams=100,
    #         protein=Decimal('24.2'),
    #         fat=Decimal('13.5'),
    #         carb=Decimal('6.2'),
    #         calories=Decimal('126.68'),
    #     )
    #     payload = {
    #         'name': 'Updated Food',
    #         'quantity_in_grams': 100,
    #         'protein': Decimal('2.6'),
    #         'fat': Decimal('31.12'),
    #         'carb': Decimal('26.91'),
    #         'calories': Decimal('245.36'),
    #     }
    #     url = create_food_detail_url(food.id)
    #     res = self.coach_client.put(url, payload)
    #     food.refresh_from_db()

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(food, k), v)

    # def test_full_update_food_fail(self):
    #     '''Test updating a food fail unauthorized.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test food123',
    #         quantity_in_grams=100,
    #         protein=Decimal('24.2'),
    #         fat=Decimal('13.5'),
    #         carb=Decimal('6.2'),
    #         calories=Decimal('126.68'),
    #     )
    #     payload = {
    #         'name': 'Updated Food',
    #         'quantity_in_grams': 100,
    #         'protein': Decimal('2.6'),
    #         'fat': Decimal('31.12'),
    #         'carb': Decimal('26.91'),
    #         'calories': Decimal('245.36'),
    #     }
    #     url = create_food_detail_url(food.id)
    #     res = self.super_client.put(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_partial_update_food_success(self):
    #     '''Test updating partially a food successfully.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test food123',
    #         quantity_in_grams=100,
    #         protein=Decimal('24.2'),
    #         fat=Decimal('13.5'),
    #         carb=Decimal('6.2'),
    #         calories=Decimal('126.68'),
    #     )
    #     payload = {
    #         'name': 'Partially Updated Food',
    #         'fat': Decimal('31.12'),
    #         'calories': Decimal('245.36'),
    #     }
    #     url = create_food_detail_url(food.id)
    #     res = self.coach_client.patch(url, payload)
    #     food.refresh_from_db()

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(food.protein, Decimal('24.2'))
    #     self.assertEqual(food.carb, Decimal('6.2'))
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(food, k), v)

    # def test_delete_food_success(self):
    #     '''Test deleting a fod instance successfully.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test food123',
    #         quantity_in_grams=100,
    #         protein=Decimal('24.2'),
    #         fat=Decimal('13.5'),
    #         carb=Decimal('6.2'),
    #         calories=Decimal('126.68'),
    #     )
    #     url = create_food_detail_url(food.id)
    #     res = self.coach_client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # def test_delete_food_fail(self):
    #     '''Test deleting a fod instance fail.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test food123',
    #         quantity_in_grams=100,
    #         protein=Decimal('24.2'),
    #         fat=Decimal('13.5'),
    #         carb=Decimal('6.2'),
    #         calories=Decimal('126.68'),
    #     )
    #     url = create_food_detail_url(food.id)
    #     res = self.normal_client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertTrue(Food.objects.filter(id=food.id).exists())

    def test_get_list_diet_success(self):
        '''Test getting all dies successfully.'''
        res = self.coach_client.get(DIET_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_list_diet_fail(self):
        '''Test getting all dies fail.'''
        res = self.normal_client.get(DIET_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_diet_success(self):
        '''Test getting detail of an object successfully.'''
        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )
        Routine.objects.create(
            diet=diet,
            week_number=1,
            day_number=1,
            description='Test Description',
            breakfast='test',
            snack_1='test',
            lunch='test',
            snack_2='test',
            dinner='test',
            snack_3='test',
        )
        url = create_diet_detail_url(diet.id)
        res = self.coach_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_detail_diet_fail(self):
        '''Test getting detail of an object fail.'''
        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )
        Routine.objects.create(
            diet=diet,
            week_number=1,
            day_number=1,
            description='Test Description',
            breakfast='test',
            snack_1='test',
            lunch='test',
            snack_2='test',
            dinner='test',
            snack_3='test',
        )
        url = create_diet_detail_url(diet.id)
        # self.normal_client and self.super_client are not the
        # creators of the diet so they cant get its details.
        res = self.normal_client.get(url)
        res_2 = self.super_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_diet_success(self):
        '''Test deleting a diet successfully.'''
        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )
        Routine.objects.create(
            diet=diet,
            week_number=1,
            day_number=1,
            description='Test Description',
            breakfast='test',
            snack_1='test',
            lunch='test',
            snack_2='test',
            dinner='test',
            snack_3='test',
        )
        url = create_diet_detail_url(diet.id)
        res = self.coach_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_diet_fail(self):
        '''Test deleting a diet fail.'''

        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )
        Routine.objects.create(
            diet=diet,
            week_number=1,
            day_number=1,
            description='Test Description',
            breakfast='test',
            snack_1='test',
            lunch='test',
            snack_2='test',
            dinner='test',
            snack_3='test',
        )
        url = create_diet_detail_url(diet.id)
        res = self.coach_client_2.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
