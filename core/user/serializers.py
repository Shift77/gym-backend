from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from . import utils


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for creating user.'''
    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'password', 'name', 'national_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        '''Creates and return user with "Encrypted" password.'''
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Update and return user with "Encrypted" password.'''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class OtpSerializer(serializers.ModelSerializer):
    '''Serializer to create an OTP for user's phone number verification.'''
    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'password']
        extra_kwargs = {
            'phone_number': {'write_only': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        user = authenticate(
            phone_number=attrs['phone_number'],
            password=attrs['password'],
        )

        if user:
            return attrs

        raise serializers.ValidationError('Bad credentials.', code=400)

    def update(self, instance, validated_data):
        otp = utils.generate_otp('12345')  # Test values
        instance.otp = otp
        instance.save()
        utils.send_otp_via_sms(otp)  # Only for TEsting the functionality.

        return instance


class VerifyOtpSerializer(serializers.ModelSerializer):
    '''Serializer to verify the OTP that has been sent for the user.'''
    class Meta:
        model = get_user_model()
        fields = ['otp']
        extra_kwargs = {
            'otp': {'write_only': True}
        }

    def validate(self, attrs):
        sent_otp = attrs['otp']
        user = self.context.get('request.user')

        if user.otp == sent_otp:
            return attrs

        raise serializers.ValidationError('Wrong OTP code.', code=400)

    def update(self, instance, validated_data):
        instance.otp = None
        instance.is_num_verified = True
        instance.save()

        return instance
