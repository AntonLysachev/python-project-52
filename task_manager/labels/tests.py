from django.test import TestCase, Client
from .models import Label
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model


class LabelTestCase(TestCase):
    def setUp(self):
        Label.objects.create(name='Label')

    def test_create_label(self):
        assert Label.objects.count() == 1

    def test_update_label(self):
        label = Label.objects.get(id=1)
        label.name = 'Name2'
        label.save()
        assert label.name == 'Name2'

    def test_delete_label(self):
        label = Label.objects.get(id=1)
        label.delete()
        assert Label.objects.count() == 0

    def test_duplicate_label(self):
        with self.assertRaises(IntegrityError):
            Label.objects.create(name='Label')


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
