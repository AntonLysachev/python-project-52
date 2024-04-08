from django.db import models
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User
from task_manager.tags.models import Tag

class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    statuses = models.ManyToManyField(Statuses)
    executor = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)