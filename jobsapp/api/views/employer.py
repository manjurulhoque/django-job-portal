from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from jobsapp.api.permissions import IsEmployer, IsJobCreator
from jobsapp.api.serializers import (
    ApplicantSerializer,
    CompanySerializer,
    CompanyWriteSerializer,
    DashboardJobSerializer,
    NewJobSerializer,
)
from jobsapp.models import Applicant, Company


class DashboardAPIView(ListAPIView):
    serializer_class = DashboardJobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.serializer_class.Meta.model.objects.none()
        return self.serializer_class.Meta.model.objects.filter(
            user_id=self.request.user.id
        ).select_related("company", "user")


class JobCreateAPIView(CreateAPIView):
    serializer_class = NewJobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployerCompanyListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CompanyWriteSerializer
        return CompanySerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Company.objects.none()
        return Company.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployerCompanyDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CompanyWriteSerializer
        return CompanySerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Company.objects.none()
        return Company.objects.filter(user=self.request.user)


class ApplicantsListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Applicant.objects.none()
        user = self.request.user
        return Applicant.objects.filter(job__user_id=user.id).select_related(
            "user", "job", "job__company"
        )


class ApplicantsPerJobListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsJobCreator]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Applicant.objects.none()
        return Applicant.objects.filter(job_id=self.kwargs["job_id"]).select_related(
            "user", "job", "job__company"
        ).order_by("id")


class UpdateApplicantStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        applicant_id = kwargs.get("applicant_id")
        status_code = kwargs.get("status_code")
        try:
            applicant = Applicant.objects.select_related("job__user").get(
                id=applicant_id
            )
        except Applicant.DoesNotExist:
            data = {"message": "Applicant not found"}
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)

        if applicant.job.user != request.user:
            data = {"errors": "You are not authorized"}
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
        if status_code not in [1, 2]:
            status_code = 3

        applicant.status = status_code
        applicant.comment = request.data.get("comment", "")
        applicant.save()
        data = {"message": "Applicant status updated"}
        return JsonResponse(data, status=status.HTTP_200_OK)
