from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from ..models import *


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Applicant
        fields = ("job_id", "user", "status")


class AppliedJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    applicant = serializers.SerializerMethodField("_applicant")

    class Meta:
        model = Job
        fields = "__all__"

    def _applicant(self, obj):
        user = self.context.get("request", None).user
        return ApplicantSerializer(Applicant.objects.get(user=user, job=obj)).data
