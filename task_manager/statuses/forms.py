from typing import Any
from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Statuses

class StatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ['name']

    def clean_name(self):
        changed_data = self.changed_data
        name = self.cleaned_data.get('name')
        if 'name' in changed_data:
            if Statuses.objects.filter(name=name).exists():
                self.add_error('name', _('A task status with the same name already exists'))
        return name
