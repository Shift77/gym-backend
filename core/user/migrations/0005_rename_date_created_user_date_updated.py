# Generated by Django 4.2.6 on 2023-10-16 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_created',
            new_name='date_updated',
        ),
    ]