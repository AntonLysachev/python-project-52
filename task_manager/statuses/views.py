from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Status
from .forms import StatusForm
from django.db.models.deletion import ProtectedError
from task_manager.mixins import LoginRequiredMixin


class StatusesIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        statuses = Status.objects.all()

        return render(request, 'statuses/index.html', context={'statuses': statuses})


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Status successfully created'))
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Status changed successfully'))
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        status = self.get_object()
        try:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
        except ProtectedError:
            messages.error(request, _('Cannot delete status because it is in use'))
            return redirect('users')
        return redirect(self.success_url)
