from typing import Any
from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Task

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def clean_name(self) -> str:
        changed_data = self.changed_data
        name = self.cleaned_data.get('name')
        if 'name' in changed_data:
            if Task.objects.filter(name=name).exists():
                self.add_error('name', _("Задача с таким именем уже существует"))
        return name