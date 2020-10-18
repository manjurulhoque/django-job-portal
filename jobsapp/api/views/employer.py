from typing import Generic, TypeVar

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from django.db.models import QuerySet

from jobsapp.api.permissions import IsEmployer
from jobsapp.api.serializers import ApplicantSerializer
from jobsapp.models import Applicant


class ApplicantsListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        return Applicant.objects.filter(job__user_id=user.id)
