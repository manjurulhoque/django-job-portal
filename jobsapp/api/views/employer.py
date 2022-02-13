from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from jobsapp.api.permissions import IsEmployer, IsJobCreator
from jobsapp.api.serializers import ApplicantSerializer, DashboardJobSerializer, NewJobSerializer
from jobsapp.models import Applicant


class DashboardAPIView(ListAPIView):
    serializer_class = DashboardJobSerializer
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


class ApplicantsPerJobListAPIView(ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsJobCreator]

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs["job_id"]).order_by("id")


class UpdateApplicantStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request, *args, **kwargs):
        applicant_id = kwargs.get("applicant_id")
        status_code = kwargs.get("status_code")
        try:
            applicant = Applicant.objects.select_related("job__user").get(id=applicant_id)
        except Applicant.DoesNotExist:
            data = {"message": "Applicant not found"}
            return JsonResponse(data, status=404)

        if applicant.job.user != request.user:
            data = {"errors": "You are not authorized"}
            return JsonResponse(data, status=403)
        if status_code not in [1, 2]:
            status_code = 3

        applicant.status = status_code
        applicant.comment = request.data.get("comment", "")
        applicant.save()
        data = {"message": "Applicant status updated"}
        return JsonResponse(data, status=200)
