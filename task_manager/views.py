from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, 'index.html')


class LoginView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы залогинены')
            return redirect('index')
        return render(request, 'login.html', {'form': form})