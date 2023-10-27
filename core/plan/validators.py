from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def custom_coach_validator(value):
    '''Validating if the model field user has is_coach as True.'''
    user = get_user_model().objects.get(id=value)
    if not user.is_coach:
        raise ValidationError('User must be a coach!')
