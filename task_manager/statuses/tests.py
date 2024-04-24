from django.test import TestCase
from .models import Statuse


class UsersTestCase(TestCase):
    def setUp(self):
        Statuse.objects.create(name='Name')

    def test_create_user(self):
        assert Statuse.objects.count() == 1

    def test_update_user(self):
        status = Statuse.objects.get(id=1)
        status.name = 'TestName2'
        assert status.name == 'TestName2'

    def test_delete_user(self):
        status = Statuse.objects.get(id=1)
        status.delete()
        assert Statuse.objects.count() == 0
