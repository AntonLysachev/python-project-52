from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class Index(TemplateView):
    template_name = 'index.html'
