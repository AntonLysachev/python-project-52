from django.test import TestCase, Client
from .models import Label
from django.urls import reverse
from django.contrib.auth import get_user_model


class LabelViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.label = Label.objects.create(name='Test Label')

    def test_label_index_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')

    def test_label_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_update', args=[self.label.id]), {
            'name': 'Updated Label',
        })
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
