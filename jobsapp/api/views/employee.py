from typing import Any

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models.query import QuerySet

from jobsapp.api.permissions import IsEmployee
from jobsapp.api.serializers import ApplicantSerializer, JobSerializer
from jobsapp.models import Applicant, Job


class ApplyJobApiView(CreateAPIView):
    serializer_class = ApplicantSerializer
    http_method_names = [u"post"]
    permission_classes = [IsAuthenticated, IsEmployee]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AppliedJobsAPIView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self) -> "QuerySet[Job]":
        applied_jobs_id = list(
            Applicant.objects.filter(user=self.request.user).values_list("job_id", flat=True)  # type: ignore
        )
        return Job.objects.filter(id__in=applied_jobs_id)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def already_applied_api_view(request: Request, job_id: int) -> Response:
    is_applied = Applicant.objects.filter(user=request.user, job_id=job_id).exists()
    content = {"is_applied": is_applied}
    return Response(content)
