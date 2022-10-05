from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import ApplicantsListAPIView
from .views import ApplicantsPerJobListAPIView
from .views import AppliedJobsAPIView
from .views import ApplyJobApiView
from .views import DashboardAPIView
from .views import JobCreateAPIView
from .views import JobViewSet
from .views import SearchApiView
from .views import UpdateApplicantStatusAPIView
from .views import already_applied_api_view
from .views import categories_list_api_view

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
    path("search/", SearchApiView.as_view()),
    path("categories/", categories_list_api_view),
    path("apply-job/<int:job_id>/", ApplyJobApiView.as_view()),
    path("applied-jobs/", AppliedJobsAPIView.as_view()),
    path("applied-for-job/<int:job_id>/", already_applied_api_view),
    path(
        "employer/",
        include(
            [
                path("dashboard/", DashboardAPIView.as_view()),
                path("jobs/create/", JobCreateAPIView.as_view()),
                path("applicants/", ApplicantsListAPIView.as_view()),
                path("applicants/<int:job_id>/", ApplicantsPerJobListAPIView.as_view()),
                path("applicants/<int:applicant_id>/<int:status_code>/update/", UpdateApplicantStatusAPIView.as_view()),
            ]
        ),
    ),
]

urlpatterns += router.urls
