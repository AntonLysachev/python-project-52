from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from task_manager.tasks.models import Task
from task_manager.fixtures.test_helpers import username, password, usertest


class UserViewsTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), usertest)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')
        user_exists = get_user_model().objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_user_update_view(self):
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_update', kwargs={'pk': user.pk}), usertest)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, 'Test')

    def test_user_delete_view_used_user(self):
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Невозможно удалить пользователя, потому что он используется')
        user_exists = get_user_model().objects.filter(username='UserTest').exists()
        self.assertTrue(user_exists)

    def test_user_delete_view(self):
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        message_texts = [str(message) for message in messages]
        self.assertIn('Пользователь успешно удален', message_texts)
        user_exists = get_user_model().objects.filter(username='UserTest').exists()
        self.assertFalse(user_exists)

    def test_user_update_view_forbidden(self):
        response = self.client.post(reverse('user_update', kwargs={'pk': 2}), usertest)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения другого пользователя')
        user = get_user_model().objects.get(pk=2)
        self.assertNotEqual(user.first_name, 'Test')

    def test_user_delete_view_forbidden(self):
        response = self.client.post(reverse('user_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения другого пользователя')
        user_exists = get_user_model().objects.filter(pk=2).exists()
        self.assertTrue(user_exists)
