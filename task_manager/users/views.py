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
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError


class BaseUserView(SuccessMessageMixin):
    model = User
    template_name = 'form.html'
    success_url = reverse_lazy('users')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(self.request, _('You do not have permission to change another user'))
            return redirect('users')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class UsersIndexView(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        users = User.objects.filter(is_active=True)
        return render(request, 'users/index.html', context={'users': users})


class UserCreateView(BaseUserView, CreateView):
    form_class = UserFormCreated
    success_url = reverse_lazy('login')
    success_message = _("User successfully registered")

    def get(self, request, *args, **kwargs):
        return super(CreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        context['button'] = 'Register'
        return context


class UserUpdateView(BaseUserView, LoginRequiredMixin, UpdateView):
    form_class = UserFormCreated
    success_message = _("User successfully changed")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change user'
        context['button'] = 'Update'
        return context


class UserDeleteView(BaseUserView, LoginRequiredMixin, DeleteView):

    template_name = 'users/delete.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        user = self.get_object()
        try:
            user.delete()
            messages.success(request, _('User successfully deleted'))
        except ProtectedError:
            messages.error(request, _('Cannot delete user because they have associated tasks'))
            return redirect('users')
        return redirect(self.success_url)
