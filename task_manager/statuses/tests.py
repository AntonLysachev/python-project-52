from django.test import TestCase, Client
from .models import Status
from django.urls import reverse
from task_manager.tasks.models import Task


class StatusViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()

    def test_status_index_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_status_create_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.login(username='UserTest', password='123')
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_update', args=[status.id]), {
            'name': 'Updated Status',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Updated Status').exists())

    def test_status_delete_view_used_status(self):
        self.client.login(username='UserTest', password='123')
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=status.id).exists())

    def test_status_delete_view(self):
        self.client.login(username='UserTest', password='123')
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())
