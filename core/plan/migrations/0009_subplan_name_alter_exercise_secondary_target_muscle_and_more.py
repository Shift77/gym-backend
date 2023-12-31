# Generated by Django 4.2.6 on 2023-10-22 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plan.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0008_alter_subplan_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='secondary_target_muscle',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_coach', to=settings.AUTH_USER_MODEL, validators=[plan.models.custom_coach_validator]),
        ),
    ]
