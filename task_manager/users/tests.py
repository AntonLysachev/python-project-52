from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserViewsTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'password1': 'testpass2',
            'password2': 'testpass2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'password1': 'testpass2',
            'password2': 'testpass2',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 0)
