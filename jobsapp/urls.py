from django.urls import path

from .views import *

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
]
