from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    JobViewSet,
    ApplyJobApiView,
    SearchApiView,
    AppliedJobsAPIView,
    already_applied_api_view,
    JobCreateAPIView,
)

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
    path("apply-job/<int:job_id>/", ApplyJobApiView.as_view()),
    path("applied-jobs/", AppliedJobsAPIView.as_view()),
    path("applied-for-job/<int:job_id>/", already_applied_api_view),
    path(
        "employer/",
        include(
            [
                path("jobs/create/", JobCreateAPIView.as_view()),
            ]
        ))
]

urlpatterns += router.urls
