# Generated by Django 4.1.7 on 2023-03-14 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_user_is_verified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False, help_text="Email activated"),
        ),
    ]
