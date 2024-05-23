from django.test import TestCase, Client
from .models import Task
from task_manager.statuses.models import Status
from django.urls import reverse


class TaskViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()

    def test_task_index_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_show_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.get(reverse('task_show', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_create_view(self):
        self.client.login(username='UserTest', password='123')
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'status': status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='UserTest', password='123')
        task = Task.objects.get(name='Test')
        status = Status.objects.get(name='Test')
        response = self.client.post(reverse('task_update', args=[task.id]), {
            'name': 'Updated Task',
            'status': status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Updated Task').exists())

    def test_task_delete_view(self):
        self.client.login(username='UserTest', password='123')
        task = Task.objects.get(name='Test')
        response = self.client.post(reverse('task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
