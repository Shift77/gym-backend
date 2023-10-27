from django.db import models
from django.conf import settings
from .validators import custom_coach_validator


class Plan(models.Model):
    '''Model for creating a plan.'''
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_coach',
        validators=[custom_coach_validator]
        )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        )
    name = models.CharField(max_length=255)
    level = models.CharField(
        max_length=255,
        default='beginner',
        )
    gender = models.CharField(
        max_length=255,
        default='No Gender Specific',
        )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    '''Model for creating exercises.'''
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    main_target_muscle = models.CharField(max_length=255)
    secondary_target_muscle = models.CharField(max_length=255,
                                               blank=True,
                                               null=True)
    description = models.TextField()
    number_of_sets = models.IntegerField(default=3)
    rep_range = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubPlan(models.Model):
    '''Model for creating sub-plans'''
    plan = models.ForeignKey(Plan,
                             on_delete=models.CASCADE,
                             related_name='sub_plans')
    name = models.CharField(max_length=255, blank=True, null=True)
    week_number = models.IntegerField()
    day_number = models.IntegerField()
    exercises = models.ManyToManyField(Exercise)
    description = models.TextField()

    def __str__(self):
        return str(self.name) + f' : day {str(self.day_number)}'
