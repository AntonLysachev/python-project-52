# Generated by Django 5.0.3 on 2024-04-03 05:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_users_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
