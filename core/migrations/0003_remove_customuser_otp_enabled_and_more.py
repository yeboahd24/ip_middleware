# Generated by Django 4.2.3 on 2023-07-27 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_customuser_otp_device_alter_customuser_groups_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="otp_enabled",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="otp_secret_key",
        ),
    ]
