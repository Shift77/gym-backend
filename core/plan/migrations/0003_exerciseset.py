# Generated by Django 4.2.6 on 2023-10-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_exercise'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('rep_range', models.CharField(max_length=255)),
                ('rest_time_between_rep', models.CharField(max_length=255)),
            ],
        ),
    ]
