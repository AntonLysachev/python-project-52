from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Status
from django import forms

class StatusForm(ModelForm):
    name = forms.CharField(label=_('Name'))
    
    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        changed_data = self.changed_data
        name = self.cleaned_data.get('name')
        if 'name' in changed_data:
            if Status.objects.filter(name=name).exists():
                self.add_error('name', _('A task status with the same name already exists'))
        return name
