import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
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
            r = f.save()
            return redirect(reverse_lazy("resume_cv:builder", kwargs={"code": r.code}))
        else:
            print(f.errors)
            return redirect(reverse_lazy("resume_cv:templates"))


def resume_builder(request, code):
    """
    Resume builder
    """
    resume = ResumeCv.objects.get(code=code)
    templates = ResumeCvTemplate.objects.all()
    token = get_token(request)
    return render(request, "resumes/builder.html", {"resume": resume, "templates": templates, "token": token})


def update_builder(request, id):
    """
    Resume builder
    """
    resume = ResumeCv.objects.get(id=id)
    if resume:
        data = json.loads(request.body)
        resume.content = data.get('gjs-html')
        resume.style = data.get('gjs-css')
        resume.save()
        return JsonResponse({
            'success': "Updated successfully",
        }, safe=True)
    return JsonResponse({
        'error': "No resume found",
    }, safe=True)


def load_builder(request, id):
    """
    Load builder
    """
    resume = ResumeCv.objects.get(id=id)
    if resume:
        return JsonResponse({
            'gjs-html': resume.content if resume.content else resume.template.content,
            'gjs-css': resume.style if resume.style else resume.template.style
        }, safe=True)
    else:
        return JsonResponse({
            'error': "No template found",
        }, safe=True)
