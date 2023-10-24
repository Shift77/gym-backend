# Generated by Django 4.2.6 on 2023-10-22 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0006_alter_subplan_exercises'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='plan',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sub_plans', to='plan.plan'),
            preserve_default=False,
        ),
    ]
