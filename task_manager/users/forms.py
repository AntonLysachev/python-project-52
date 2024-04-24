from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserFormCreated(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'), help_text=_('Your password must contain at least 3 characters'), min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Password confirmation'), help_text=_('To confirm, please enter your password again'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def clean_username(self) -> str:
        changed_data = self.changed_data
        username = self.cleaned_data.get('username')
        if 'username' in changed_data:
            if User.objects.filter(username=username).exists():
                self.add_error('username', _("A user with the same name already exists"))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            self.add_error('password2', _("The entered passwords do not match"))
        for field in self.fields:
            data = cleaned_data.get(field)
            if data == '':
                self.add_error(field, _('Обязательное поле'))
