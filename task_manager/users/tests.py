from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UsersTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='TestName', 
                            last_name='TestLastName', 
                            username='TestUser', 
                            password=make_password('password'))

    def test_create_user(self):
        assert User.objects.count() == 1
    
    def test_update_user(self):
        user = User.objects.get(id=1)
        user.first_name = 'TestName2'
        assert user.first_name == 'TestName2'

    def test_delete_user(self):
        user = User.objects.get(id=1)
        user.delete()
        assert User.objects.count() == 0