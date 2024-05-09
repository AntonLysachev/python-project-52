from django import forms
from django.forms import ModelForm, Form
from django.utils.translation import gettext_lazy as _
from .models import Task
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(ModelForm):
    name = forms.CharField(label=_("Name"))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label=_("Status"))
    description = forms.CharField(widget=forms.Textarea, required=False, label=_("Description"))
    executor = UserChoiceField(queryset=User.objects.filter(is_active=True),
                               required=False, label=_("Executor"))
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all(),
                                            required=False, label=_("Labels"))

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


class TaskFilterForm(Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    required=False,
                                    label=_('Status'))
    executor = UserChoiceField(queryset=User.objects.filter(is_active=True),
                               required=False, label=_('Executor'))
    labels = forms.ModelChoiceField(queryset=Label.objects.all(), required=False, label=_('Label'))
    self_tasks = forms.BooleanField(required=False, label=_('Only self tasks'))
