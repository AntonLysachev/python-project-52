from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError


class UsersTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='TestName',
                            last_name='TestLastName',
                            username='TestUser',
                            password=make_password('password'))
        user = User.objects.get(id=1)

        Status.objects.create(name='Status')
        status = Status.objects.get(id=1)

        Task.objects.create(name='Task',
                            description='description',
                            autor=user,
                            status=status,
                            executor=user)

    def test_create_user(self):
        assert User.objects.count() == 1

    def test_update_user(self):
        user = User.objects.get(id=1)
        user.first_name = 'TestName2'
        user.save()
        assert user.first_name == 'TestName2'

    def test_rotected_error(self):
        with self.assertRaises(ProtectedError):
            user = User.objects.get(id=1)
            user.delete()

    def test_delete_user(self):
        task = Task.objects.get(id=1)
        task.delete()
        user = User.objects.get(id=1)
        user.delete()
        assert User.objects.count() == 0

    def test_duplicate_user(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(username='TestUser', password=make_password('password'))
