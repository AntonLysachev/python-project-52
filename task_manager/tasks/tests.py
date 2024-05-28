from django.test import TestCase, Client
from django.contrib.messages import get_messages
from .models import Task
from task_manager.statuses.models import Status
from django.urls import reverse
from task_manager.fixtures.test_helpers import username, password


class TaskViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_task_index_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_show_view(self):
        response = self.client.get(reverse('task_show', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_create_view(self):
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'status': status.id,
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        task = Task.objects.get(name='Test')
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('task_update', args=[task.id]), {
            'name': 'Updated Task',
            'status': status.id,
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')
        self.assertTrue(Task.objects.filter(name='Updated Task').exists())

    def test_task_delete_view(self):
        task = Task.objects.get(name='Test')
        response = self.client.post(reverse('task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')
        self.assertFalse(Task.objects.filter(id=task.id).exists())
