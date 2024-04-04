from typing import Any
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
