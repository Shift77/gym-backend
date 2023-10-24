from django.test import TestCase
from django.contrib.auth import get_user_model
from plan import models


def create_exercise(name: str):
    exercise = models.Exercise.objects.create(
        name=name,
        main_target_muscle='First body part',
        secondary_target_muscle='second body part',
        description='Exercise description!',
        number_of_sets=3,
        rep_range='8-12',
    )
    return exercise


class ModelTests(TestCase):
    '''Tests for plan models.'''
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            phone_number='123431098',
            password='testpass123'
        )

    def test_create_plan_success(self):
        '''Test creating a plan instance.'''
        new_user = get_user_model().objects.create_user(
            phone_number='1234321',
            password='testpass123'
        )
        plan = models.Plan.objects.create(
            coach=self.user,  # This should cause an error as
                              # self.user's is_coach is False!
            target_user=new_user,
            name='Test Plan',
            level='Beginner',
            description='Test description of the plan!'
        )

        self.assertEqual(plan.coach, self.user)
        self.assertEqual(plan.target_user, new_user)
        self.assertEqual(plan.level, 'Beginner')
        self.assertTrue(models.Plan.objects.filter(id=plan.id).exists())

    def test_create_exercise_success(self):
        '''Test creating a exercise.'''
        exercise = models.Exercise.objects.create(
            name='Test Exercise',
            main_target_muscle='Test body part',
            secondary_target_muscle='second body part',
            description='Exercise description!',
            number_of_sets=3,
            rep_range='8-12',
        )

        self.assertEqual(str(exercise), 'Test Exercise')
        self.assertEqual(exercise.description, 'Exercise description!')
        self.assertTrue(models.Exercise.objects.filter(id=exercise.id).exists())

    # def test_create_exercise_set_success(self):
    #     '''Test creating a set'''
    #     new_set = models.ExerciseSet.objects.create(
    #         order=1,
    #         rep_range='8-12',
    #         rest_time_between_rep='1-2 min',
    #     )

    #     self.assertEqual(str(new_set), '1')
    #     self.assertEqual(new_set.rep_range, '8-12')
    #     self.assertTrue(models.ExerciseSet.objects.filter(id=new_set.id).exists())

    def test_create_sub_plan_success(self):
        '''Test creating a sub-plan instance.'''
        new_user = get_user_model().objects.create_user(
            phone_number='1234321',
            password='testpass123'
        )
        plan = models.Plan.objects.create(
            coach=self.user,
            target_user=new_user,
            name='Test Plan',
            level='Beginner',
            description='Test description of the plan!'
        )
        e_dict = {}

        for i in range(4):
           e_dict[i] = create_exercise(('Exercise' + str(i+1)))

        sub_plan = models.SubPlan.objects.create(
            plan=plan,
            name='Push',
            week_number=1,
            day_number=1,
            description='Day description!',
        )
        sub_plan.exercises.set(e_dict.values())

        self.assertTrue(models.SubPlan.objects.filter(id=sub_plan.id).exists())
        self.assertEqual(sub_plan.week_number, 1)
