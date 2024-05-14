from django.test import TestCase
from .models import Status
from task_manager.tasks.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError


class StatusTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='TestName',
                            last_name='TestLastName',
                            username='TestUser',
                            password=make_password('password'))
        user = User.objects.get(id=1)

        Status.objects.create(name='Name')
        status = Status.objects.get(id=1)

        Task.objects.create(name='Task',
                            autor=user,
                            status=status)

    def test_create_status(self):
        assert Status.objects.count() == 1

    def test_update_status(self):
        status = Status.objects.get(id=1)
        status.name = 'Name2'
        status.save()
        assert status.name == 'Name2'

    def test_delete_exception_status(self):
        with self.assertRaises(ProtectedError):
            status = Status.objects.get(id=1)
            status.delete()

    def test_delete_status(self):
        task = Task.objects.get(id=1)
        task.delete()
        status = Status.objects.get(id=1)
        status.delete()
        assert Status.objects.count() == 0

    def test_duplicate_label(self):
        with self.assertRaises(IntegrityError):
            Status.objects.create(name='Name')
