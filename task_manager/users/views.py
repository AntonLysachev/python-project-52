from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserFormCreated
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError


class UsersIndexView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        users = User.objects.filter(is_active=True)
        return render(request, 'users/index.html', context={'users': users})


class UserCreateView(CreateView):
    model = User
    form_class = UserFormCreated
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully registered'))
        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserFormCreated
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully changed'))
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        user = self.get_object()
        try:
            user.delete()
            messages.success(request, _('User successfully deleted'))
        except ProtectedError:
            messages.error(request, _('Cannot delete user because they have associated tasks'))
            return redirect('users')
        return redirect(self.success_url)
