from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.
class TemplateListView(LoginRequiredMixin, ListView):
    """
    Get list of templates to create resume/cv
    """
