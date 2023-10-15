from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''User manager for custom user model.'''
    def create_user(self, password, phone_number, **extra_fields):
        '''Function to create a normal user.'''
        if not phone_number:
            raise ValueError('Phone number must be set.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, password, phone_number, **extra_fields):
        '''Function to create Superuser.'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_coach', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))

        return self.create_user(password, phone_number, **extra_fields)
