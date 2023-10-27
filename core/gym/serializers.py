from rest_framework import serializers
from . import models


class ReviewSerializer(serializers.ModelSerializer):
    '''Serializer for Review model.'''
    class Meta:
        model = models.Review
        fields = ['id', 'author', 'gym', 'name', 'description']
        read_only_fields = ['id', 'author']


class SocialSerializer(serializers.ModelSerializer):
    '''Serializer for Social model.'''
    class Meta:
        model = models.Social
        fields = ['id', 'gym', 'name', 'link']
        read_only_fields = ['id', 'gym']


class GymSerializer(serializers.ModelSerializer):
    '''Serializer for Gym model.'''
    review = ReviewSerializer(many=True, read_only=True)
    social = SocialSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Gym
        fields = [
            'id',
            'name',
            'number',
            'address',
            'owner',
            'days_closed',
            'hour_open',
            'hour_close',
            'description',
            'review',
            'social',  # Make the gym field of social "read_only" on
                       # this serializer
        ]
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        '''Create a gym instance with optional social instances. :)'''
        if 'social' in validated_data.keys():
            social_data = validated_data.pop('social')
        else:
            social_data = False

        user = self.context['user']
        new_gym = models.Gym.objects.create(owner=user, **validated_data)

        if social_data:
            for s_data in social_data:
                models.Social.objects.create(
                    gym=new_gym,
                    **s_data,
                )

        return new_gym

    def update(self, instance, validated_data):
        if 'social' in validated_data.keys():
            validated_data.pop('social')

        return super().update(instance, validated_data)
