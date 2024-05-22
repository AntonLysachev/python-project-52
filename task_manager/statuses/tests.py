from django.test import TestCase, Client
from .models import Status
from django.urls import reverse
from django.contrib.auth import get_user_model


class StatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.status = Status.objects.create(name='Test Status')

    def test_status_index_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_update', args=[self.status.id]), {
            'name': 'Updated Status',
        })
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
