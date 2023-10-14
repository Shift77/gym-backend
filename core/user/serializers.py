from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from . import models
from . import utils

class PendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PendingUser
        fields = ['phone_number', 'national_id', 'name', 'password']

    def validate(self, attrs):
        '''
        Validate if user already exists.
        '''
        phone_number = attrs.get('phone_number')
        User = get_user_model()
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {'error': 'Phone number already exists.'},
                code=400
            )
        return super().validate(attrs)

    def create(self, validated_data):
        '''
        Create and return a PendingUser and send otp to their phone number to verify.
        '''
        otp = utils.generate_otp()
        phone_number = validated_data.get('phone_number')
        pending_user, _ = models.PendingUser.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'phone_number': phone_number,
                'otp': otp,
                'national_id': validated_data.get('national_id'),
                'name': validated_data.get('name'),
                'date_joined' :datetime.now(timezone.utc),
                'password': make_password(validated_data.get('password')),
            }
        )
        utils.send_otp(phone_num=phone_number, otp=otp)
        return pending_user
