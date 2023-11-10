# Generated by Django 4.2.6 on 2023-11-09 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plan.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0011_alter_plan_target_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'verbose_name': 'تمرین', 'verbose_name_plural': 'تمرین ها'},
        ),
        migrations.AlterModelOptions(
            name='plan',
            options={'verbose_name': 'برنامه ورزشی', 'verbose_name_plural': 'برنامه های ورزشی'},
        ),
        migrations.AlterModelOptions(
            name='subplan',
            options={'verbose_name': 'روتین ورزشی', 'verbose_name_plural': 'روتین های ورزشی'},
        ),
        migrations.AlterField(
            model_name='exercise',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='سازنده'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='main_target_muscle',
            field=models.CharField(max_length=255, verbose_name='عضلات هدف اولیه'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='number_of_sets',
            field=models.IntegerField(default=3, verbose_name='تعداد ست'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='rep_range',
            field=models.CharField(max_length=100, verbose_name='بازه تکرار'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='secondary_target_muscle',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='عضلات هدف ثانویه'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_coach', to=settings.AUTH_USER_MODEL, validators=[plan.validators.custom_coach_validator], verbose_name='مربی'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='gender',
            field=models.CharField(default='No Gender Specific', max_length=255, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='level',
            field=models.CharField(default='beginner', max_length=255, verbose_name='سطح'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='target_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='شاگرد'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='day_number',
            field=models.IntegerField(verbose_name='روز'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='exercises',
            field=models.ManyToManyField(to='plan.exercise', verbose_name='تمرین ها'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_plans', to='plan.plan', verbose_name='برنامه ورزشی'),
        ),
        migrations.AlterField(
            model_name='subplan',
            name='week_number',
            field=models.IntegerField(verbose_name='هفته'),
        ),
    ]