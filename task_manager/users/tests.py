from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
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


users = json.loads(get_content(build_fixture_path('user2.json')))
user3 = users['user3']
user4 = users['user4']


class UserViewsTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
       
    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), user3)
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(username = 'testuser3').exists()
        self.assertFalse(user_exists)

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': 1}), user4)
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(pk = 1)
        self.assertEqual(user.first_name, 'Test4')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        user_exists = get_user_model().objects.filter(username = 'testuser').exists()
        self.assertFalse(user_exists)

    def test_user_update_view_forbidden(self):

        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': 2}), user3)
        self.assertEqual(response.status_code, 302)

