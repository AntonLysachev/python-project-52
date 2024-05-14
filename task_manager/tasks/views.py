from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from .forms import TaskForm, TaskFilterForm
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.contrib import messages
from task_manager.mixins import LoginRequiredMixin


class BaseTasksView(TemplateView):

    def get_context(self) -> dict:
        context = {}
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.filter(is_active=True)
        context['labels'] = Label.objects.all()
        context['form'] = TaskForm
        return context


class TasksIndexView(LoginRequiredMixin, BaseTasksView):

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
            if form.cleaned_data.get('labels'):
                tasks = tasks.filter(labels=form.cleaned_data['labels'])
            if form.cleaned_data['self_tasks']:
                tasks = tasks.filter(autor=request.user)
            context['form'] = form
            context['tasks'] = tasks
        return render(request, 'tasks/index.html', context=context)


class TaskShowView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        task_dict = model_to_dict(task)
        task_dict['autor'] = f"{task.autor.first_name} {task.autor.last_name}"
        task_dict['status'] = task.status
        if task.executor:
            task_dict['executor'] = f"{task.executor.first_name} {task.executor.last_name}"
        else:
            task_dict['executor'] = None
        task_dict['created_at'] = task.created_at
        return render(request, 'tasks/show.html', context=task_dict)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _('Task created successfully'))
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('The task was successfully modified'))
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        task = self.get_object()
        if task.autor == request.user:
            task.delete()
            messages.success(request, _('Task successfully deleted'))
        else:
            messages.error(request, _('Only its author can delete a task'))
        return redirect(self.success_url)
