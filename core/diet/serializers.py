from rest_framework import serializers
from .models import Diet, Routine

# class FoodSerializer(serializers.ModelSerializer):
#     '''Serializer for Food model.'''
#     class Meta:
#         model = Food
#         fields = '__all__'
#         read_only_fields = ['id', 'created_by']


class RoutineSerializer(serializers.ModelSerializer):
    '''Serializer for Routine model.'''
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Routine
        fields = [
            'id',
            'name',
            'week_number',
            'day_number',
            'description',
            'breakfast',
            'snack_1',
            'lunch',
            'snack_2',
            'dinner',
            'snack_3',
        ]
        read_only_fields = ['id', 'diet']


class DietSerializer(serializers.ModelSerializer):
    '''Serializer for Diet model.'''
    routine = RoutineSerializer(many=True)

    class Meta:
        model = Diet
        fields = [
            'id',
            'coach',
            'target_user',
            'name',
            'level',
            'purpose',
            'description',
            'routine'
        ]
        read_only_fields = ['id', 'coach']

    def create(self, validated_data):
        routines_data = validated_data.pop('routine', False)
        user = self.context['user']
        new_diet = Diet.objects.create(coach=user, **validated_data)

        if routines_data:
            for routine in routines_data:
                routine.pop('id', None)  # Ignore id on create.
                Routine.objects.create(
                    diet=new_diet,
                    **routine
                    )

        return new_diet

    def update(self, instance, validated_data):
        routines_data = validated_data.pop('routine', False)
        instance = super().update(instance, validated_data)

        # getting all routines id of a diet.
        existing_routines_id = [r.id for r in instance.routine.all()]

        if routines_data:

            for routine in routines_data:

                if routine.get('id', None) in existing_routines_id:
                    routine_instance = Routine.objects.get(
                        id=routine.get('id')
                        )
                    routine_instance.name = routine.get(
                        'name',
                        routine_instance.name
                        )
                    routine_instance.week_number = routine.get(
                        'week_number',
                        routine_instance.week_number
                        )
                    routine_instance.day_number = routine.get(
                        'day_number',
                        routine_instance.day_number
                        )
                    routine_instance.description = routine.get(
                        'description',
                        routine_instance.description
                        )
                    routine_instance.breakfast = routine.get(
                        'breakfast',
                        routine_instance.breakfast
                        )
                    routine_instance.snack_1 = routine.get(
                        'snack_1',
                        routine_instance.snack_1
                        )
                    routine_instance.lunch = routine.get(
                        'lunch',
                        routine_instance.lunch
                        )
                    routine_instance.snack_2 = routine.get(
                        'snack_2',
                        routine_instance.snack_2)
                    routine_instance.dinner = routine.get(
                        'dinner',
                        routine_instance.dinner
                        )
                    routine_instance.snack_3 = routine.get(
                        'snack_3',
                        routine_instance.snack_3
                        )
                    routine_instance.save()
                else:
                    routine.pop('id', None)  # removing id on create
                    Routine.objects.create(
                        diet=instance,
                        **routine
                    )

        return instance
