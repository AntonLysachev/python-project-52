from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Statuses
from .forms import StatusForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class StatusesIndexView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        if request.user.is_authenticated:
            statuses = Statuses.objects.filter(is_active=True)
            
            return render(request, 'statuses/index.html', context={'statuses': statuses})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect('login')

class StatusCreateView(TemplateView):

    context = {'url_name': 'status_create',
               'head': _('Create status'),
               'button': _('Create')}
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            form = StatusForm()
            self.context['form'] = form
            return render(request, 'statuses/form.html', self.context)
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect('login')

    def post(self, request, *args, **kwargs) -> HttpRequest:
        form = StatusForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect('statuses')
        
        return render(request, 'statuses/form.html', self.context)


class StatusUpdateView(TemplateView):
    context = {'url_name': 'status_update',
               'head': _('Edit status'),
               'button': _('Edit')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        if request.user.is_authenticated:
            status_id = kwargs.get('id')
            status = Statuses.objects.get(id=status_id)
            form = StatusForm(instance=status)
            self.context['form'] = form
            self.context['id'] = status_id
            return render(request, 'statuses/form.html', self.context)
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect('login')
    
    def post(self, request, *args, ** kwargs) -> HttpRequest:

        status_id = kwargs.get('id')
        status = Statuses.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        self.context['form'] = form
        self.context['id'] = status_id
        if form.is_valid():
            form.save()
            messages.success(request, _('Статус успешно изменен'))
            return redirect('statuses')
        return render(request, 'statuses/form.html', self.context)
    
class StatusDeleteView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        if request.user.is_authenticated:
            status_id = kwargs.get('id')
            status = Statuses.objects.get(id=status_id)
            name = status.name
            return render(request, 'statuses/delete.html', context={'name': name, 'id': status_id})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect('login')
    
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Statuses.objects.get(id=status_id)
        # if status.task_set.exists():
        #     messages.error(request, _('Невозможно удалить статус, потому что он используется'))
        #     redirect('statuses')
        status.is_active = False
        status.save()
        messages.success(request, _('Status deleted successfully'))
        return redirect('statuses')


