from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from categories.models import Category
from categories.serializers import CategorySerializer
from tags.api.serializers import TagSerializer

from ..models import Applicant, Company, Job


class CompanySerializer(serializers.ModelSerializer):
    size_display = serializers.CharField(source="get_size_display", read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "slug",
            "tagline",
            "description",
            "website",
            "logo",
            "industry",
            "headquarters",
            "size",
            "size_display",
            "culture_benefits",
            "is_verified",
            "featured",
            "linkedin_url",
            "facebook_url",
            "cover_image",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "description",
            "website",
            "logo",
            "industry",
            "size",
            "culture_benefits",
            "tagline",
            "headquarters",
            "linkedin_url",
            "facebook_url",
            "cover_image",
        )
        read_only_fields = ("id",)


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    job_tags = serializers.SerializerMethodField()
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    workplace_type_display = serializers.CharField(source="get_workplace_type_display", read_only=True)
    experience_level_display = serializers.CharField(source="get_experience_level_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    salary_period_display = serializers.CharField(source="get_salary_period_display", read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    def get_job_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data


class DashboardJobSerializer(JobSerializer):
    total_candidates = serializers.SerializerMethodField()

    class Meta(JobSerializer.Meta):
        fields = "__all__"

    def get_total_candidates(self, obj):
        return obj.applicants.count()


class NewJobSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Job
        fields = (
            "id",
            "company",
            "category",
            "title",
            "description",
            "responsibilities",
            "requirements",
            "location",
            "type",
            "workplace_type",
            "experience_level",
            "application_deadline",
            "website",
            "status",
            "salary",
            "salary_min",
            "salary_max",
            "salary_currency",
            "salary_period",
            "tags",
            "vacancy",
            "is_featured",
        )
        read_only_fields = ("id",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            self.fields["company"].queryset = Company.objects.filter(user=request.user)

    def validate_company(self, company):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        if company.user_id != request.user.id:
            raise serializers.ValidationError("You can only post jobs for your own companies.")
        return company

    def to_representation(self, instance):
        return JobSerializer(instance, context=self.context).data


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ("job",)

    def validate(self, attrs):
        if Applicant.objects.filter(user=self.context.get("request", None).user, job=attrs.get("job")).exists():
            raise serializers.ValidationError("You have already applied to this job")
        return attrs


class ApplicantSerializer(serializers.ModelSerializer):
    applied_user = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = (
            "id",
            "job_id",
            "applied_user",
            "job",
            "status",
            "created_at",
            "comment",
        )

    def get_status(self, obj):
        return obj.get_status

    def get_job(self, obj):
        return JobSerializer(obj.job, context=self.context).data

    def get_applied_user(self, obj):
        return UserSerializer(obj.user).data


class AppliedJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    applicant = serializers.SerializerMethodField("_applicant")

    class Meta:
        model = Job
        fields = "__all__"

    def _applicant(self, obj):
        user = self.context.get("request", None).user
        return ApplicantSerializer(Applicant.objects.get(user=user, job=obj), context=self.context).data
