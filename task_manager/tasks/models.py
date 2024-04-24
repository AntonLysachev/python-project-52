from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    autor = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='executed_tasks', null=True, on_delete=models.PROTECT)
    description = models.TextField(default='description', blank=True)
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name