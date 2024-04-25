from django.test import TestCase
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class TaskTestCase(TestCase):
    def setUp(self):

        User.objects.create(first_name='TestName',
                            last_name='TestLastName',
                            username='TestUser',
                            password=make_password('password'))
        user = User.objects.get(id=1)

        Status.objects.create(name='Status')
        status = Status.objects.get(id=1)

        Label.objects.create(name='Label')
        label = Label.objects.get(id=1)

        Task.objects.create(name='Task',
                            description='description',
                            status=status,
                            autor=user,
                            executor=user)
        task = Task.objects.get(id=1)
        task.labels.add(label)

    def test_create_user(self):
        assert Task.objects.count() == 1

    def test_update_user(self):
        task = Task.objects.get(id=1)
        task.name = 'Task2'
        task.save()
        assert task.name == 'Task2'

    def test_delete_user(self):
        task = Task.objects.get(id=1)
        task.delete()
        assert Task.objects.count() == 0
