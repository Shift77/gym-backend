from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''
    Custom user manager for custom user model.
    '''
    def create_user(self, name,  phone_number, national_id, password, **extra_fields):
        '''
        Create and save a user with phone number instead of username.
        '''
        if not phone_number:
            raise ValueError('Phone number must be set.')
        if not password:
            raise ValueError('Password must be set.')

        user = self.model(
            phone_number=phone_number,
            name=name,
            national_id=national_id,
            **extra_fields,
            )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, phone_number, national_id,
                     password, **extra_fields):
        '''
        Create and save a Superuser with phone number instead of username.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_coach', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superuser.')

        if extra_fields.get('is_coach') is not True:
            raise ValueError('Superuser must be a coach.')

        return self.create_user(name, phone_number, national_id,
                                password, **extra_fields)
