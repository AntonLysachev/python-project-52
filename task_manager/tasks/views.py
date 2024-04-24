from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from .forms import TaskForm, TaskFilterForm
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseTasksView(TemplateView):

    def get_context(self) -> dict:
        context = {}
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.filter(is_active=True)
        context['labels'] = Label.objects.all()
        context['form'] = TaskForm
        return context


class TasksIndexView(LoginRequiredMixin, BaseTasksView):

    login_url = '/login/'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context()
        context['tasks'] = Task.objects.all()
        context['form'] = TaskFilterForm
        form = TaskFilterForm(request.GET)
        form.is_valid()
        if form.changed_data:
            tasks = Task.objects.all()
            if form.cleaned_data['status']:
                tasks = tasks.filter(status=form.cleaned_data.get('status'))
            if form.cleaned_data['executor']:
                tasks = tasks.filter(executor=form.cleaned_data['executor'])
            if form.cleaned_data.get('label'):
                tasks = tasks.filter(label=form.cleaned_data['label'])
            if form.cleaned_data['self_tasks']:
                tasks = tasks.filter(autor=request.user)
            context['form'] = form
            context['tasks'] = tasks
        return render(request, 'tasks/index.html', context=context)
    

class TaskCreateView(LoginRequiredMixin, BaseTasksView):

    login_url = '/login/'

    context = {'url_name': 'task_create',
               'title': _('Create task'),
               'button': _('Create')}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.context.update(self.get_context())
        return render(request, 'tasks/form.html', context=self.context)
    
    def post(self, request, *args, **kwargs):

        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.autor = request.user
            task.save()
            task.status = form.cleaned_data.get('status')
            task.executor = form.cleaned_data.get('executor')
            return redirect('tasks')
        self.context['form'] = form
        return render(request, 'tasks/form.html', context=self.context)
    

class TaskShowView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        task_dict = model_to_dict(task)
        task_dict['autor'] = task.autor
        task_dict['status'] = task.status
        task_dict['executor'] = task.executor
        task_dict['created_at'] = task.created_at
        return render(request, 'tasks/show.html', context=task_dict)
    

class TaskUpdateView(LoginRequiredMixin, BaseTasksView):

    login_url = '/login/'

    context = {'url_name': 'task_update',
               'title': _('Update task'),
               'button': _('Update')}
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        self.context['form'] = form
        self.context['id'] = task_id
        return render(request, 'tasks/form.html', context=self.context)
    
    def post(self, request: HttpRequest, *args, ** kwargs) -> HttpRequest:
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        self.context['form'] = form
        self.context['id'] = task_id
        if form.is_valid():
            form.save()
            messages.success(request, _('The task was successfully modified'))
            return redirect('tasks')
        return render(request, 'tasks/form.html', self.context)
    

class TaskDeleteView(LoginRequiredMixin, BaseTasksView):

    login_url = '/login/'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        task_id = kwargs.get('id')
        task = model_to_dict(Task.objects.get(id=task_id))
        return render(request, 'tasks/delete.html', context=task)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpRequest:

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)

        if task.autor == request.user:
            task.delete()
            messages.success(request, _('Task successfully deleted'))
        else:
            messages.error(request, _('Only its author can delete a task'))
        return redirect('tasks')