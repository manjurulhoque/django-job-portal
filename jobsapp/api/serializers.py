from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from tags.api.serializers import TagSerializer
from ..models import *


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job_tags = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_job_tags(self, obj):
        if obj.tags:
            return TagSerializer(obj.tags.all(), many=True).data
        else:
            return None


class NewJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

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
