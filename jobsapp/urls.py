from django.urls import path

from .views import *

app_name = "jobs"

urlpatterns = [
    path('', index, name='home'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
]
