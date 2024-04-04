from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserFormCreated
from django.contrib.auth.hashers import make_password


class IndexView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        users = User.objects.all()
        return render(request, 'users/index.html', context={'users': users,})
    

class CreateView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = UserFormCreated()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserFormCreated(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data.get('password1'))
            user.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('login')
        return render(request, 'users/create.html', {'form': form})
    

class UpdateView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_id = kwargs.get('id')
        user = User.objects.get(pk=user_id)
        form = UserFormCreated(instance=user)
        return render(request, 'users/create.html', {"form": form})
