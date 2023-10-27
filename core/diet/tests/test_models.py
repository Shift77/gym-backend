from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from diet.models import Diet, Routine


class ModelTests(TestCase):
    '''Test models of diet app.'''
    def setUp(self):
        self.coach_user = get_user_model().objects.create_user(
            phone_number='23123123',
            password='testpass123',
            is_coach=True,
        )
        self.normal_user = get_user_model().objects.create_user(
            phone_number='97650977123',
            password='testpass123',
        )

    def test_create_diet_success(self):
        '''Test creating a diet instance successfully.'''
        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )

        self.assertTrue(Diet.objects.filter(id=diet.id).exists())
        self.assertEqual(diet.coach, self.coach_user)
        self.assertEqual(diet.purpose, 'Burning fat')
        self.assertEqual(diet.name, 'Diet')

    def test_create_diet_fail(self):
        '''Test creating a diet instance fail.'''
        diet = Diet.objects.create(
            coach=self.normal_user,  # Normal user cant create diet!
            target_user=self.coach_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )

        with self.assertRaises(ValidationError):
            diet.full_clean()

    # def test_create_food_success(self):
    #     '''Test creating a food instance.'''
    #     food = Food.objects.create(
    #         created_by=self.coach_user,
    #         name='Test Food',
    #         quantity_in_grams=100,
    #         protein=Decimal('26.3'),
    #         fat=Decimal('4.2'),
    #         carb=Decimal('45.8'),
    #         calories=Decimal('328.9'),
    #     )
    #     obj = Food.objects.get(id=food.id)

    #     self.assertTrue(Food.objects.filter(id=food.id).exists())
    #     self.assertEqual(obj.protein, Decimal('26.3'))

    def test_create_routine_success(self):
        '''Test creating a routine instance.'''
        diet = Diet.objects.create(
            coach=self.coach_user,
            target_user=self.normal_user,
            name='Diet',
            purpose='Burning fat',
            level='Beginner',
            description='Test description.',
        )

        routine = Routine.objects.create(
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

        self.assertTrue(Routine.objects.filter(id=routine.id).exists())
