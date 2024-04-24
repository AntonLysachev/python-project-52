from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, 'index.html')


class LoginView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if 'next' in request.GET:
            messages.error(request, _('You are not authorized! Please log in'))
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, _('You are logged in'))
            return redirect('index')
        form.add_error(None, _("Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру"))
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, _('You are logged out'))
    return redirect('index')
