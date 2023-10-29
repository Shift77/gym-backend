from django.db import models
from django.conf import settings
from .validators import custom_coach_validator


class Plan(models.Model):
    '''Model for creating a plan.'''
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_coach',
        validators=[custom_coach_validator],
        verbose_name='مربی'
        )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='شاگرد'
        )
    name = models.CharField(max_length=255, verbose_name='نام')
    level = models.CharField(
        max_length=255,
        default='beginner',
        verbose_name='سطح'
        )
    gender = models.CharField(
        max_length=255,
        default='No Gender Specific',
        verbose_name='جنسیت'
        )
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='توضیحات')

    class Meta:
        verbose_name = 'برنامه ورزشی'
        verbose_name_plural = 'برنامه های ورزشی'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    '''Model for creating exercises.'''
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='سازنده'
    )
    name = models.CharField(max_length=255, verbose_name='نام')
    main_target_muscle = models.CharField(max_length=255,
                                          verbose_name='عضلات هدف اولیه')
    secondary_target_muscle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='عضلات هدف ثانویه'
        )
    description = models.TextField(verbose_name='توضیحات')
    number_of_sets = models.IntegerField(default=3, verbose_name='تعداد ست')
    rep_range = models.CharField(max_length=100, verbose_name='بازه تکرار')

    class Meta:
        verbose_name = 'تمرین'
        verbose_name_plural = 'تمرین ها'

    def __str__(self):
        return self.name


class SubPlan(models.Model):
    '''Model for creating sub-plans'''
    plan = models.ForeignKey(Plan,
                             on_delete=models.CASCADE,
                             related_name='sub_plans',
                             verbose_name='برنامه ورزشی')
    name = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            verbose_name='نام')
    week_number = models.IntegerField(verbose_name='هفته')
    day_number = models.IntegerField(verbose_name='روز')
    exercises = models.ManyToManyField(Exercise, verbose_name='تمرین ها')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'روتین ورزشی'
        verbose_name_plural = 'روتین های ورزشی'

    def __str__(self):
        return str(self.name) + f' : day {str(self.day_number)}'
