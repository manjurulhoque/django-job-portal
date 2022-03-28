from django.urls import include, path

from .views import (
    TemplateListView,
)

app_name = "resume_cv"

urlpatterns = [
    path("", TemplateListView.as_view(), name="templates"),
]
