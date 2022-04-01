from django.urls import path

from .views import (
    TemplateListView,
    ResumeCVCreateView,
)

app_name = "resume_cv"

urlpatterns = [
    path("templates", TemplateListView.as_view(), name="templates"),
    path("resume-cv/create", ResumeCVCreateView.as_view(), name="resume-cv.create"),
]
