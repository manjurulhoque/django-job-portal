import json

from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from jobsapp.decorators import user_is_employee

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
        data["categories"] = ResumeCvCategory.objects.all()
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
        resume.content = data.get("gjs-html")
        resume.style = data.get("gjs-css")
        resume.save()
        return JsonResponse(
            {
                "success": "Updated successfully",
            },
            safe=True,
        )
    return JsonResponse(
        {
            "error": "No resume found",
        },
        safe=True,
    )


def load_builder(request, id):
    """
    Load builder
    """
    resume = ResumeCv.objects.get(id=id)
    if resume:
        return JsonResponse(
            {
                "gjs-html": resume.content if resume.content else resume.template.content,
                "gjs-css": resume.style if resume.style else resume.template.style,
            },
            safe=True,
        )
    else:
        return JsonResponse(
            {
                "error": "No template found",
            },
            safe=True,
        )


class UserResumeListView(ListView):
    model = ResumeCv
    template_name = "resumes/user_resumes.html"
    context_object_name = "resumes"

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by("-id")


@login_required
@user_is_employee
def download_resume(request, id):
    resume = ResumeCv.objects.get(id=id)
    if resume:
        # Font is not working in pdf
        font_config = FontConfiguration()
        css = CSS(
            string=f"""
                    @font-face {{
                        font-family: "Font Awesome 5 Brands";
                        font-style: normal;
                        font-weight: 400;
                        src: url("{static('webfonts/fa-brands-400.eot')}");
                        src: url("{static('webfonts/fa-brands-400.eot?#iefix')}") format("embedded-opentype"),
                             url("{static('webfonts/fa-brands-400.woff2')}") format("woff2"),
                             url("{static('webfonts/fa-brands-400.woff')}") format("woff"),
                             url("{static('webfonts/fa-brands-400.ttf')}") format("truetype"),
                             url("{static('webfonts/fa-brands-400.svg#fontawesome')}") format("svg");
                    }}
                    @font-face {{
                        font-family: "Font Awesome 5 Free";
                        font-style: normal;
                        font-weight: 400;
                        src: url("{static('webfonts/fa-regular-400.eot')}");
                        src: url("{static('webfonts/fa-regular-400.eot?#iefix')}") format("embedded-opentype"),
                             url("{static('webfonts/fa-regular-400.woff2')}") format("woff2"),
                             url("{static('webfonts/fa-regular-400.woff')}") format("woff"),
                             url("{static('webfonts/fa-regular-400.ttf')}") format("truetype"),
                             url("{static('webfonts/fa-regular-400.svg#fontawesome')}") format("svg");
                    }}
                    @font-face {{
                        font-family: "Font Awesome 5 Free";
                        font-style: normal;
                        font-weight: 900;
                        src: url("{static('webfonts/fa-solid-900.eot')}");
                        src: url("{static('webfonts/fa-solid-900.eot?#iefix')}") format("embedded-opentype"),
                             url("{static('webfonts/fa-solid-900.woff2')}") format("woff2"),
                             url("{static('webfonts/fa-solid-900.woff')}") format("woff"),
                             url("{static('webfonts/fa-solid-900.ttf')}") format("truetype"),
                             url("{static('webfonts/fa-solid-900.svg#fontawesome')}") format("svg");
                    }}
                    .fa, .fas {{
                        font-family: "Font Awesome 5 Free";
                        font-weight: 900;
                        font-style: normal;
                    }}
                    .far {{
                        font-family: "Font Awesome 5 Free";
                        font-weight: 400;
                        font-style: normal;
                    }}
                    .fab {{
                        font-family: "Font Awesome 5 Brands";
                        font-weight: 400;
                        font-style: normal;
                    }}""",
            font_config=font_config,
        )

        pdf_file = HTML(string=resume.content, encoding="utf-8").write_pdf(stylesheets=[css], font_config=font_config)
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{resume.name}.pdf"'
        return response
    return redirect("resume_cv:resumes")
