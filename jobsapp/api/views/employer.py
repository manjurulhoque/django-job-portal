from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from jobsapp.api.permissions import IsEmployer
from jobsapp.api.serializers import ApplicantSerializer, NewJobSerializer, JobSerializer
from jobsapp.models import Applicant


class DashboardAPIView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(user_id=self.request.user.id)


class JobCreateAPIView(CreateAPIView):
    serializer_class = NewJobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]


class ApplicantsListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        user = self.request.user
        return Applicant.objects.filter(job__user_id=user.id)
