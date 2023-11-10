# Generated by Django 4.2.6 on 2023-11-09 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plan.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diet', '0006_remove_routine_breakfast_remove_routine_dinner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diet',
            options={'verbose_name': 'برنامه غذایی', 'verbose_name_plural': 'برنامه های غذایی'},
        ),
        migrations.AlterModelOptions(
            name='routine',
            options={'verbose_name': 'روتین غذایی', 'verbose_name_plural': 'روتین های غذایی'},
        ),
        migrations.AlterField(
            model_name='diet',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_diets', to=settings.AUTH_USER_MODEL, validators=[plan.validators.custom_coach_validator], verbose_name='مربی'),
        ),
        migrations.AlterField(
            model_name='diet',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='diet',
            name='level',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='سطح'),
        ),
        migrations.AlterField(
            model_name='diet',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='diet',
            name='purpose',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='هدف'),
        ),
        migrations.AlterField(
            model_name='diet',
            name='target_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='شاگرد'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='breakfast',
            field=models.CharField(max_length=500, verbose_name='صبحانه'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='day_number',
            field=models.IntegerField(verbose_name='روز'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='diet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routine', to='diet.diet', verbose_name='برنامه غذایی'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='dinner',
            field=models.CharField(max_length=500, verbose_name='شام'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='lunch',
            field=models.CharField(max_length=500, verbose_name='ناهار'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='snack_1',
            field=models.CharField(max_length=500, verbose_name='میان وعده اول'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='snack_2',
            field=models.CharField(max_length=500, verbose_name='میان وعده دوم'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='snack_3',
            field=models.CharField(max_length=500, verbose_name='میان وعده سوم'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='week_number',
            field=models.IntegerField(verbose_name='هفته'),
        ),
    ]