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


class DashboardJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job_tags = serializers.SerializerMethodField()
    total_candidates = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_job_tags(self, obj):
        if obj.tags:
            return TagSerializer(obj.tags.all(), many=True).data
        else:
            return None

    def get_total_candidates(self, obj):
        return obj.applicants.count()


class NewJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = "__all__"


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ("job",)


class ApplicantSerializer(serializers.ModelSerializer):
    applied_user = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = ("id", "job_id", "applied_user", "job", "status", "created_at", "comment")

    def get_status(self, obj):
        return obj.get_status

    def get_job(self, obj):
        return JobSerializer(obj.job).data

    def get_applied_user(self, obj):
        return UserSerializer(obj.user).data


class AppliedJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    applicant = serializers.SerializerMethodField("_applicant")

    class Meta:
        model = Job
        fields = "__all__"

    def _applicant(self, obj):
        user = self.context.get("request", None).user
        return ApplicantSerializer(Applicant.objects.get(user=user, job=obj)).data
