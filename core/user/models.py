from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom User model.'''
    phone_number = models.CharField(max_length=15,
                                    unique=True,
                                    verbose_name='شماره تلفن')
    national_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name='کد ملی'
        )
    name = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            verbose_name='نام')
    otp = models.CharField(max_length=6,
                           blank=True,
                           null=True,
                           verbose_name='رمز یک بار مصرف')
    date_joined = models.DateTimeField(auto_now_add=True,
                                       verbose_name='تاریخ ثبت نام')
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name='تاریخ بروزرسانی')
    is_num_verified = models.BooleanField(default=False,
                                          verbose_name='تايید شماره تلفن')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='ادمین')
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='ابر ادمین')
    is_coach = models.BooleanField(default=False, verbose_name='مربی')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.phone_number}: {self.name}'
