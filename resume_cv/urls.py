from django.urls import path

from .views import (
    TemplateListView,
    ResumeCVCreateView,
    resume_builder,
    UserResumeListView,
    download_resume,
)

app_name = "resume_cv"

urlpatterns = [
    path("templates", TemplateListView.as_view(), name="templates"),
    path("resume-cv/create", ResumeCVCreateView.as_view(), name="create"),
    path("templates/builder/<code>", resume_builder, name="builder"),
    path("resumes/", UserResumeListView.as_view(), name="resumes"),
    path("download-as-pdf/<int:id>/", download_resume, name="export.pdf"),
]
