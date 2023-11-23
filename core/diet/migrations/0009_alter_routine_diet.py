# Generated by Django 4.2.7 on 2023-11-23 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0008_alter_diet_target_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='diet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='diet.diet', verbose_name='برنامه غذایی'),
        ),
    ]
