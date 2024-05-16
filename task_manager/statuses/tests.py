from django.test import TestCase, Client
from .models import Status
from task_manager.tasks.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model


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


class StatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', 
                                                         password='testpass')
        self.status = Status.objects.create(name='Test Status')

    def test_status_index_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_update', args=[self.status.id]), {
            'name': 'Updated Status',
        })
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
