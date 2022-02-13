from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobsapp.api.permissions import IsEmployee
from jobsapp.api.serializers import ApplicantSerializer, AppliedJobSerializer, ApplyJobSerializer, JobSerializer
from jobsapp.models import Applicant, Job


class ApplyJobApiView(CreateAPIView):
    serializer_class = ApplyJobSerializer
    http_method_names = [u"post"]
    permission_classes = [IsAuthenticated, IsEmployee]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AppliedJobsAPIView(ListAPIView):
    serializer_class = AppliedJobSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        applied_jobs_id = list(Applicant.objects.filter(user=self.request.user).values_list("job_id", flat=True))
        return Job.objects.filter(id__in=applied_jobs_id)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def already_applied_api_view(request, job_id):
    is_applied = Applicant.objects.filter(user=request.user, job_id=job_id).exists()
    content = {"is_applied": is_applied}
    return Response(content)
