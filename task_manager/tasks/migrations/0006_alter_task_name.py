# Generated by Django 5.0.3 on 2024-05-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0005_alter_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]