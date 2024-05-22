from django.test import TestCase, Client
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.urls import reverse
from django.contrib.auth import get_user_model


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')
        self.task = Task.objects.create(
            name='Task',
            description='Test Description',
            status=self.status,
            autor=self.user,
            executor=self.user
        )
        self.task.labels.add(self.label)

    def test_task_index_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_show_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task_show', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
