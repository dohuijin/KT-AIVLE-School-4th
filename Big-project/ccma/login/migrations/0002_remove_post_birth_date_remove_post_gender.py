# Generated by Django 4.2 on 2023-12-28 06:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="birth_date",
        ),
        migrations.RemoveField(
            model_name="post",
            name="gender",
        ),
    ]
