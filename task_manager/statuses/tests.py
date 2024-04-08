from django.test import TestCase
from .models import Statuses

class UsersTestCase(TestCase):
    def setUp(self):
        Statuses.objects.create(name='Name')

    def test_create_user(self):
        assert Statuses.objects.count() == 1
    
    def test_update_user(self):
        status = Statuses.objects.get(id=1)
        status.name = 'TestName2'
        assert status.name == 'TestName2'

    def test_delete_user(self):
        status = Statuses.objects.get(id=1)
        status.delete()
        assert Statuses.objects.count() == 0
