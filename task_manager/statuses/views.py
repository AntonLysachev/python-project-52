from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Status
from .forms import StatusForm
from django.db.models.deletion import ProtectedError
from task_manager.mixins import LoginRequiredMixin


class StatusesIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        statuses = Status.objects.all()

        return render(request, 'statuses/index.html', context={'statuses': statuses})


class StatusCreateView(LoginRequiredMixin, TemplateView):

    context = {'url_name': 'status_create',
               'title': _('Create status'),
               'button': _('Create')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        form = StatusForm()
        self.context['form'] = form

        return render(request, 'statuses/form.html', self.context)

    def post(self, request, *args, **kwargs) -> HttpRequest:
        form = StatusForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect('statuses')

        return render(request, 'statuses/form.html', self.context)


class StatusUpdateView(LoginRequiredMixin, TemplateView):

    context = {'url_name': 'status_update',
               'title': _('Edit status'),
               'button': _('Update')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(instance=status)
        self.context['form'] = form
        self.context['id'] = status_id

        return render(request, 'statuses/form.html', self.context)

    def post(self, request, *args, ** kwargs) -> HttpRequest:

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        self.context['form'] = form
        self.context['id'] = status_id
        if form.is_valid():
            form.save()
            messages.success(request, _('Status changed successfully'))
            return redirect('statuses')
        return render(request, 'statuses/form.html', self.context)


class StatusDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        name = status.name
        return render(request, 'statuses/delete.html', context={'name': name, 'id': status_id})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        try:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
        except ProtectedError:
            messages.error(request, _('Cannot delete status because it is in use'))
        return redirect('statuses')
