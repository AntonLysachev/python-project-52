# Generated by Django 5.0.3 on 2024-04-09 03:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0008_remove_task_label_task_labels"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="autor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="autor_tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
