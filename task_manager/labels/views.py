from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Label
from .forms import LabelForm
from task_manager.mixins import LoginRequiredMixin


class LabelsIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        labels = Label.objects.all()

        return render(request, 'labels/index.html', context={'labels': labels})


class LabelCreateView(LoginRequiredMixin, TemplateView):

    context = {'url_name': 'label_create',
               'title': _('Create label'),
               'button': _('Create')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        form = LabelForm()
        self.context['form'] = form

        return render(request, 'labels/form.html', self.context)

    def post(self, request, *args, **kwargs) -> HttpRequest:
        form = LabelForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully created'))
            return redirect('labels')

        return render(request, 'labels/form.html', self.context)


class LabelUpdateView(LoginRequiredMixin, TemplateView):

    context = {'url_name': 'label_update',
               'title': _('Update label'),
               'button': _('Update')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(instance=label)
        self.context['form'] = form
        self.context['id'] = label_id

        return render(request, 'labels/form.html', self.context)

    def post(self, request, *args, ** kwargs) -> HttpRequest:

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        self.context['form'] = form
        self.context['id'] = label_id
        if form.is_valid():
            form.save()
            messages.success(request, _('Label changed successfully'))
            return redirect('labels')
        return render(request, 'labels/form.html', self.context)


class LabelDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        name = label.name
        return render(request, 'labels/delete.html', context={'name': name, 'id': label_id})

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        tasks = label.task_set.all()
        if tasks:
            messages.error(request, _('Cannot delete label because it is in use'))
        else:
            label.delete()
            messages.success(request, _('Label deleted successfully'))

        return redirect('labels')
