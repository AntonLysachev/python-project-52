from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserFormCreated(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label=_('Name'))
    last_name = forms.CharField(max_length=150, required=True, label=_('Last name'))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'),
                                help_text=_('Your password must contain at least 3 characters'),
                                min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Password confirmation'),
                                help_text=_('To confirm, please enter your password again'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
