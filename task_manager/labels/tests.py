from django.test import TestCase, Client
from .models import Label
from django.urls import reverse
from task_manager.tasks.models import Task
from django.contrib.messages import get_messages
from task_manager.fixtures.test_helpers import username, password


class LabelViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_label_index_view(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_label_create_view(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label',
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно создана')
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_update', args=[label.id]), {
            'name': 'Updated Label',
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно изменена')
        self.assertTrue(Label.objects.filter(name='Updated Label').exists())

    def test_label_delete_view_used_label(self):
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_delete', args=[label.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить метку, потому что она используется')
        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_label_delete_view(self):
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        label = Label.objects.get(name='Test')
        response = self.client.post(reverse('label_delete', args=[label.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        message_texts = [str(message) for message in messages]
        self.assertIn('Метка успешно удалена', message_texts)
        self.assertFalse(Label.objects.filter(id=label.id).exists())
