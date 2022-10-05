from django.urls import path

from .views import ResumeCVCreateView
from .views import TemplateListView
from .views import load_builder
from .views import resume_builder

app_name = "resume_cv"

urlpatterns = [
    path("templates", TemplateListView.as_view(), name="templates"),
    path("resume-cv/create", ResumeCVCreateView.as_view(), name="create"),
    path("templates/builder/<code>", resume_builder, name="builder"),
]
