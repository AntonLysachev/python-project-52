from django.test import TestCase, Client
from .models import Label
from django.urls import reverse
from task_manager.tasks.models import Task


class LabelViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()

    def test_label_index_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_label_create_view(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        self.client.login(username='UserTest', password='123')
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_update', args=[label.id]), {
            'name': 'Updated Label',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Updated Label').exists())

    def test_label_delete_view_used_label(self):
        self.client.login(username='UserTest', password='123')
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_delete', args=[label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_label_delete_view(self):
        self.client.login(username='UserTest', password='123')
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_delete', args=[label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label.id).exists())
