from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Task
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from .forms import TaskForm


class TasksIndexView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        tasks = Task.objects.all()
        statuses = Statuses.objects.filter(is_active=True)
        executors = User.objects.filter(is_active=True)
        print(tasks)
        return render(request, 'tasks/index.html', context={'tasks': tasks, 
                                                            'statuses': statuses,
                                                            'executors': executors})
    

class TaskCreateView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        statuses = Statuses.objects.filter(is_active=True)
        executors = User.objects.filter(is_active=True)
        label = Label.objects.all()
        return render(request, 'tasks/create.html', context={'label': label, 
                                                             'statuses': statuses,
                                                             'executors': executors})
    def post(self, request, *args, **kwargs):

        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.autor = request.user
            task.save()
            task.status.set(form.cleaned_data.get('status'))
            task.executor.set(form.cleaned_data.get('executor'))
            return redirect('tasks')
        statuses = Statuses.objects.filter(is_active=True)
        executors = User.objects.filter(is_active=True)
        label = Label.objects.all()
        return render(request, 'tasks/create.html', context={'form': form,
                                                             'label': label, 
                                                             'statuses': statuses,
                                                             'executors': executors,})