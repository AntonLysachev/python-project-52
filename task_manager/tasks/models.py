from django.db import models
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=150)
    status = models.ManyToManyField(Statuses)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor_tasks')
    executor = models.ManyToManyField(User, related_name='executed_tasks', default=User, blank=True)
    description = models.TextField(default='description', blank=True)
    labels = models.TextField(default='labels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)