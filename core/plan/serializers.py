from rest_framework import serializers
from . import models

class ExerciseSerializer(serializers.ModelSerializer):
    '''Serializer for Exercise model.'''
    class Meta:
        model = models.Exercise
        fields = '__all__'
        read_only_fields = ['id', 'created_by']


class SubPlanSerializer(serializers.ModelSerializer):
    '''Serializer for Sub-plan model.'''
    exercises = ExerciseSerializer(many=True, read_only=True)
    exercises_id_list = serializers.ListField(write_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.SubPlan
        fields = [
            'id',
            'plan',
            'name',
            'week_number',
            'day_number',
            'exercises',
            'exercises_id_list'
        ]
        read_only_fields = ['id', 'plan']

class PlanSerializer(serializers.ModelSerializer):
    '''Serializer for Plan model.'''
    sub_plans = SubPlanSerializer(many=True)
    class Meta:
        model = models.Plan
        fields = [
            'id',
            'coach',
            'target_user',
            'name',
            'level',
            'gender',
            'description',
            'sub_plans',
        ]
        read_only_fields = ['id', 'coach']

    def create(self, validated_data):
        '''Create a Plan instance with Sub-plan instances.'''
        sub_plans_data = validated_data.pop('sub_plans', False)

        user = self.context['user']
        new_plan = models.Plan.objects.create(coach=user, **validated_data)

        if sub_plans_data:

            for sub_plan in sub_plans_data:
                sub_plan.pop('id', None)  # removing id field in create.
                exercises_id_list = sub_plan.pop('exercises_id_list', False)

                new_sub_plan = models.SubPlan.objects.create(
                    plan=new_plan,
                    **sub_plan,
                )
                if exercises_id_list:
                    id_list = [id for id in exercises_id_list if
                            models.Exercise.objects.filter(id=id).exists()]
                    new_sub_plan.exercises.set(id_list)

        return new_plan

    def update(self, instance, validated_data):
        sub_plans_data = validated_data.pop('sub_plans', False)  # A list
        print(validated_data)
        instance = super().update(instance, validated_data)

        existing_sub_plans_id = [e.id for e in instance.sub_plans.all()]

        if sub_plans_data:
            for sub_plan_d in sub_plans_data:
                print(sub_plan_d)
                exercises_id_list = sub_plan_d.pop('exercises_id_list', False)

                if sub_plan_d.get('id', None) in existing_sub_plans_id:
                    sub_plan_instance = models.SubPlan.objects.get(id=sub_plan_d.get('id'))
                    sub_plan_instance.name = sub_plan_d.get('name', sub_plan_instance.name)
                    sub_plan_instance.week_number = sub_plan_d.get('week_number', sub_plan_instance.week_number)
                    sub_plan_instance.day_number = sub_plan_d.get('day_number', sub_plan_instance.day_number)
                    sub_plan_instance.description = sub_plan_d.get('description', sub_plan_instance.description)
                    if exercises_id_list:
                        valid_id_list = [id for id in exercises_id_list if
                                models.Exercise.objects.filter(id=id).exists()]
                        sub_plan_instance.exercises.set(valid_id_list)

                    sub_plan_instance.save()
                else:
                    sub_plan_d.pop('id', None)
                    sub_plan_instance = models.SubPlan.objects.create(
                        plan=instance,
                        **sub_plan_d
                    )
                    if exercises_id_list:
                        valid_id_list = [id for id in exercises_id_list if
                                models.Exercise.objects.filter(id=id).exists()]
                        sub_plan_instance.exercises.set(valid_id_list)

                    sub_plan_instance.save()

        return instance
