from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from datetime import datetime, timezone


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user with phone number and national id.
    '''
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_coach = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self) -> str:
        return self.name


class PendingUser(User):
    '''Pending user model for otp verification.'''
    def is_valid(self):
        """10 mins OTP validation"""
        lifespan_in_seconds = float(settings.OTP_EXPIRE_TIME * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.date_joined
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return
