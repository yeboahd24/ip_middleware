# Generated by Django 4.2.3 on 2023-07-27 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_remove_customuser_otp_enabled_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
