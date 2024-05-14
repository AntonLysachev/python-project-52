from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Label
from .forms import LabelForm
from task_manager.mixins import LoginRequiredMixin


class LabelsIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        labels = Label.objects.all()

        return render(request, 'labels/index.html', context={'labels': labels})


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully created'))
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _('Label changed successfully'))
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        label = self.get_object()
        if label.task_set.all():
            messages.error(request, _('Cannot delete label because it is in use'))
        else:
            label.delete()
            messages.success(request, _('Label deleted successfully'))
        return redirect(self.success_url)
