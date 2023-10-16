from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserADmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserADmin):
    '''User admin panel.'''
    model = User
    ordering = ['id']
    list_display = ['phone_number', 'name', 'national_id']
    fieldsets = [
        (None, {'fields': ('phone_number', 'name', 'national_id')}),
        ('Permissions',
            {'fields': ('is_coach', 'is_num_verified', 'is_active', 'is_staff',
                        'is_superuser')}),
        ('Dates', {'fields': ('lat_login', 'date_joined', 'date_updated')})
    ]
    add_fieldsets = [
        (None, {
            'fields':
            ('phone_number', 'password1', 'password2', 'name', 'national_id',),
            'classes': ('wide',),
            }),
        ('Permissions',
            {'fields': ('is_coach', 'is_active', 'is_staff', 'is_superuser'),
             'classes': ('wide',)
             }),
    ]

    readonly_fields = ['last_login', 'date_joined', 'date_updated']
