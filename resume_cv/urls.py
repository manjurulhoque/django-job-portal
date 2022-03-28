from django.urls import include, path

from .views import *

app_name = "resume_cv::"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
