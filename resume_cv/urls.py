from django.urls import path

from .views import (
    TemplateListView,
    ResumeCVCreateView,
    resume_builder,
    load_builder,
)

app_name = "resume_cv"

urlpatterns = [
    path("templates", TemplateListView.as_view(), name="templates"),
    path("resume-cv/create", ResumeCVCreateView.as_view(), name="create"),
    path("templates/builder/<code>", resume_builder, name="builder"),
]
