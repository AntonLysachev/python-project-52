from django.test import TestCase, Client
from .models import Status
from django.urls import reverse
from task_manager.tasks.models import Task
from django.contrib.messages import get_messages
from task_manager.fixtures.test_helpers import username, password


class StatusViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_status_index_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_status_create_view(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status',
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_update', args=[status.id]), {
            'name': 'Updated Status',
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')
        self.assertTrue(Status.objects.filter(name='Updated Status').exists())

    def test_status_delete_view_used_status(self):
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить статус, потому что он используется')
        self.assertTrue(Status.objects.filter(id=status.id).exists())

    def test_status_delete_view(self):
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('status_delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        message_texts = [str(message) for message in messages]
        self.assertIn('Статус успешно удален', message_texts)
        self.assertFalse(Status.objects.filter(id=status.id).exists())
