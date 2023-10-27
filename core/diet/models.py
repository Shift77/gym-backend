from django.db import models
from django.conf import settings
from plan.validators import custom_coach_validator


class Diet(models.Model):
    '''Model to store diet objects.'''
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_diets',
        validators=[custom_coach_validator]
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


# class Food(models.Model):
#     '''Model to store food objects.'''
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='created_foods',
#         validators=[custom_coach_validator]
#     )
#     name = models.CharField(max_length=255)
#     quantity_in_grams = models.IntegerField()
#     protein = models.DecimalField(max_digits=5, decimal_places=2)
#     fat = models.DecimalField(max_digits=5, decimal_places=2)
#     carb = models.DecimalField(max_digits=5, decimal_places=2)
#     calories = models.DecimalField(max_digits=7, decimal_places=3)

#     def __str__(self):
#         return f'{str(self.name)} : {str(self.quantity_in_grams)} grams'


class Routine(models.Model):
    '''Model to store diet objects.'''
    diet = models.ForeignKey(
        Diet,
        on_delete=models.CASCADE,
        related_name='routine'
        )
    name = models.CharField(max_length=255)
    week_number = models.IntegerField()
    day_number = models.IntegerField()
    description = models.TextField()
    breakfast = models.CharField(max_length=500)
    snack_1 = models.CharField(max_length=500)
    lunch = models.CharField(max_length=500)
    snack_2 = models.CharField(max_length=500)
    dinner = models.CharField(max_length=500)
    snack_3 = models.CharField(max_length=500)

    def __str__(self):
        return f'{str(self.name)} : day {str(self.day_number)}'
