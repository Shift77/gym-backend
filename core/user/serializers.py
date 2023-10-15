from django.contrib.auth import get_user_model
from rest_framework import serializers


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
