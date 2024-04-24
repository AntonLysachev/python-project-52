from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Label
from django import forms


class LabelForm(ModelForm):

    name = forms.CharField(label=_('Name'))

    class Meta:
        model = Label
        fields = ['name']

    def clean_name(self):
        changed_data = self.changed_data
        name = self.cleaned_data.get('name')
        if 'name' in changed_data:
            if Label.objects.filter(name=name).exists():
                self.add_error('name', _('A task status with the same name already exists'))
        return name
