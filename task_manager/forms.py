from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.ModelForm):
    username = forms.CharField(help_text='', label=_('User name'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))

    class Meta:
        model = User
        fields = ['username', 'password']
