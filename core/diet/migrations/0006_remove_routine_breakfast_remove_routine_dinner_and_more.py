# Generated by Django 4.2.6 on 2023-10-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0005_food_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='breakfast',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='dinner',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='lunch',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='snack_1',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='snack_2',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='snack_3',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.AddField(
            model_name='routine',
            name='breakfast',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routine',
            name='dinner',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routine',
            name='lunch',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routine',
            name='snack_1',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routine',
            name='snack_2',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routine',
            name='snack_3',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
    ]