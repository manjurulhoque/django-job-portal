from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from resume_cv.models import ResumeCvTemplate, ResumeCvCategory


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
