from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
import os
import json

TESTS_DIR = os.path.dirname(os.path.dirname(__file__))
FIXTURES_PATH = f"{TESTS_DIR}/fixtures"


def build_fixture_path(file_name):
    return os.path.join(FIXTURES_PATH, file_name)


def get_content(addres):
    with open(addres, 'r') as f:
        data = f.read()
        return data


usertest = json.loads(get_content(build_fixture_path('usertest.json')))


class UserViewsTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), usertest)
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_user_update_view(self):
        self.client.login(username='UserTest', password='123')
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_update', kwargs={'pk': user.pk}), usertest)
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, 'Test')

    def test_user_delete_view_used_user(self):
        self.client.login(username='UserTest', password='123')
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(username='UserTest').exists()
        self.assertTrue(user_exists)

    def test_user_delete_view(self):
        self.client.login(username='UserTest', password='123')
        task = Task.objects.get(name='Test')
        self.client.post(reverse('task_delete', args=[task.id]))
        user = get_user_model().objects.get(username='UserTest')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(username='UserTest').exists()
        self.assertFalse(user_exists)

    def test_user_update_view_forbidden(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.post(reverse('user_update', kwargs={'pk': 2}), usertest)
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(pk=2)
        self.assertNotEqual(user.first_name, 'Test')

    def test_user_delete_view_forbidden(self):
        self.client.login(username='UserTest', password='123')
        response = self.client.post(reverse('user_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(pk=2).exists()
        self.assertTrue(user_exists)
