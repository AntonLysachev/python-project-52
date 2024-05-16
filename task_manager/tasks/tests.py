from django.test import TestCase, Client
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict


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

    def test_add_label_to_task(self):
        task = Task.objects.get(id=1)
        label2 = Label.objects.create(name='Label2')
        task.labels.add(label2)
        assert label2 in task.labels.all()

    def test_remove_label_from_task(self):
        task = Task.objects.get(id=1)
        label = Label.objects.get(id=1)
        task.labels.remove(label)
        assert label not in task.labels.all()

    def test_change_task_status(self):
        task = Task.objects.get(id=1)
        status2 = Status.objects.create(name='Status2')
        task.status = status2
        task.save()
        assert task.status == status2

    def test_create_task_without_status(self):
        user = User.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            Task.objects.create(name='Task2',
                                description='description2',
                                autor=user,
                                executor=user)


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
            'title': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())