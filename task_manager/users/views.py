from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserFormCreated
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixin
from django.db.models import ProtectedError


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

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, _('User successfully deleted'))
        except ProtectedError:
            messages.error(request, _('Cannot delete user because they have associated tasks.'))
            return redirect('users')
        return response
    


# class UserCreateView(TemplateView):

#     context = {'url_name': 'user_create',
#                'head': _('Sign up'),
#                'button': _('Register')}

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

#         form = UserFormCreated()
#         self.context['form'] = form
#         return render(request, 'users/form.html', self.context)

#     def post(self, request, *args, **kwargs) -> HttpRequest:

#         form = UserFormCreated(request.POST)
#         self.context['form'] = form
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data.get('password1'))
#             user.save()
#             messages.success(request, _('User successfully registered'))

#             return redirect('login')

#         return render(request, 'users/form.html', self.context)



# class UserUpdateView(LoginRequiredMixin, TemplateView):

#     context = {'url_name': 'user_update',
#                'head': _('Change user'),
#                'button': _('Update')}

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

#         self.request_user = request.user
#         user_id = kwargs.get('id')
#         user = User.objects.get(id=user_id)

#         if self.request_user == user:

#             form = UserFormCreated(instance=user)
#             self.context['form'] = form
#             self.context['id'] = user_id

#             return render(request, 'users/form.html', self.context)
#         messages.error(request, _('You do not have permission to change another user'))
#         return redirect('users')

#     def post(self, request, *args, **kwargs) -> HttpRequest:

#         user_id = kwargs.get('id')
#         user = User.objects.get(id=user_id)
#         form = UserFormCreated(request.POST, instance=user)
#         self.context['form'] = form
#         self.context['id'] = user_id

#         if form.is_valid():

#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data.get('password1'))
#             user.save()
#             messages.success(request, _('User successfully changed'))
#             return redirect('users')

#         return render(request, 'users/form.html', self.context)


# class UserDeleteView(LoginRequiredMixin, TemplateView):

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

#         user_id = kwargs.get('id')
#         user = User.objects.get(id=user_id)

#         if request.user == user:

#             full_name = f'{user.first_name} {user.last_name}'
#             context = {'id': user_id,
#                        'full_name': full_name}

#             return render(request, 'users/delete.html', context)
#         messages.error(request, _('You do not have permission to change another user'))
#         return redirect('users')

#     def post(self, request, *args, **kwargs):

#         user_id = kwargs.get('id')
#         user = User.objects.get(id=user_id)
#         user.is_active = False
#         user.save()
#         messages.success(request, _('User successfully deleted'))
#         return redirect('users')
