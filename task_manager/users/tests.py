from django.test import TestCase, Client
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.urls import reverse
from django.contrib.auth import get_user_model


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


class UserViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'password1': 'testpass2',
            'password2': 'testpass2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'testpass2',
            'password2': 'testpass2',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 0)
