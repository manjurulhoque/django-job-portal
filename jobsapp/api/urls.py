from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    ApplicantsListAPIView,
    ApplicantsPerJobListAPIView,
    AppliedJobsAPIView,
    ApplyJobApiView,
    DashboardAPIView,
    JobCreateAPIView,
    JobViewSet,
    SearchApiView,
    UpdateApplicantStatusAPIView,
    already_applied_api_view,
)

app_name = "jobs-api"

router = DefaultRouter()
router.register("jobs", JobViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Django Job Portal API",
        default_version="v1",
        description="Django job portal API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="manzurulhoquerumi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("search/", SearchApiView.as_view(), name="search"),
    path("apply-job/<int:job_id>/", ApplyJobApiView.as_view(), name="apply-job"),
    path("applied-jobs/", AppliedJobsAPIView.as_view(), name="applied-jobs"),
    path("applied-for-job/<int:job_id>/", already_applied_api_view, name="applied-for-job"),
    path(
        "employer/",
        include(
            [
                path("dashboard/", DashboardAPIView.as_view(), name="employer-dashboard"),
                path("jobs/create/", JobCreateAPIView.as_view(), name="employer-job-create"),
                path("applicants/", ApplicantsListAPIView.as_view(), name="employer-applicants-list"),
                path("applicants/<int:job_id>/", ApplicantsPerJobListAPIView.as_view(), name="employer-applicants-per-job-list"),
                path("applicants/<int:applicant_id>/<int:status_code>/update/", UpdateApplicantStatusAPIView.as_view(), name="employer-update-applicant-status"),
            ]
        ),
    ),
]

urlpatterns += router.urls
