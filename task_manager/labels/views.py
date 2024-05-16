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
from django.contrib.messages.views import SuccessMessageMixin


class BaseLabelView(LoginRequiredMixin, SuccessMessageMixin):
    model = Label
    template_name = 'form.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class LabelsIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        labels = Label.objects.all()

        return render(request, 'labels/index.html', context={'labels': labels})


class LabelCreateView(BaseLabelView, CreateView):
    form_class = LabelForm
    success_message = _('Label successfully created')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create label'
        context['button'] = 'Create'
        return context


class LabelUpdateView(BaseLabelView, UpdateView):
    form_class = LabelForm
    success_message = _('Label changed successfully')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update label'
        context['button'] = 'Update'
        return context


class LabelDeleteView(BaseLabelView, DeleteView):
    template_name = 'labels/delete.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        label = self.get_object()
        if label.task_set.all():
            messages.error(request, _('Cannot delete label because it is in use'))
        else:
            label.delete()
            messages.success(request, _('Label deleted successfully'))
        return redirect(self.success_url)
