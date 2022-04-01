from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

# Create your views here.
from jobsapp.mixins import EmployeeRequiredMixin
from resume_cv.forms import ResumeCvForm
from resume_cv.models import ResumeCvTemplate, ResumeCvCategory, ResumeCv


class TemplateListView(ListView):
    """
    Get list of templates to create resume/cv
    """
    model = ResumeCvTemplate
    context_object_name = "templates"
    template_name = "resumes/templates.html"

    def get_queryset(self):
        return self.model.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = ResumeCvCategory.objects.all()
        return data


class ResumeCVCreateView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    """
    Create resume/cv
    """
    form_class = ResumeCvForm

    def post(self, request):
        f = ResumeCvForm(request.POST)
        if f.is_valid():
            f.instance.user = request.user
            f.save()
        else:
            print(f.errors)
        return HttpResponse('This is a post only view')
