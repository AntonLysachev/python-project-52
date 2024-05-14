from django.test import TestCase
from .models import Label
from django.db import IntegrityError


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
