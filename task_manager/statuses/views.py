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
from django.contrib.messages.views import SuccessMessageMixin


class BaseStatusView(LoginRequiredMixin, SuccessMessageMixin):
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class StatusesIndexView(BaseStatusView, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        statuses = Status.objects.all()

        return render(request, 'statuses/index.html', context={'statuses': statuses})


class StatusCreateView(BaseStatusView, CreateView):
    form_class = StatusForm
    success_message = _('Status successfully created')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create status'
        context['button'] = 'Create'
        return context


class StatusUpdateView(BaseStatusView, UpdateView):
    form_class = StatusForm
    success_message = _('Status changed successfully')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update status'
        context['button'] = 'Update'
        return context


class StatusDeleteView(BaseStatusView, DeleteView):
    template_name = 'statuses/delete.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        status = self.get_object()
        try:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
        except ProtectedError:
            messages.error(request, _('Cannot delete status because it is in use'))
        return redirect(self.success_url)
