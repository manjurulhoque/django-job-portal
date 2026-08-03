from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from jobsapp.api.serializers import CompanySerializer, JobSerializer
from jobsapp.models import Company, Job


class JobPagination(PageNumberPagination):
    page_size = 9


class CompanyPagination(PageNumberPagination):
    page_size = 12


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    queryset = (
        Job.objects.unfilled()
        .select_related("company", "user", "category")
        .prefetch_related("tags")
    )
    permission_classes = [AllowAny]
    pagination_class = JobPagination

    def get_queryset(self):
        qs = super().get_queryset()
        company_id = self.request.query_params.get("company")
        if company_id:
            qs = qs.filter(company_id=company_id)
        category = self.request.query_params.get("category")
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=category)
            else:
                qs = qs.filter(category__slug=category)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(title__icontains=q)
        location = self.request.query_params.get("location")
        if location:
            qs = qs.filter(location__icontains=location)
        return qs


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-featured", "-created_at")
    permission_classes = [AllowAny]
    pagination_class = CompanyPagination

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        industry = self.request.query_params.get("industry")
        if industry:
            qs = qs.filter(industry__icontains=industry)
        featured = self.request.query_params.get("featured")
        if featured in ("1", "true", "True"):
            qs = qs.filter(featured=True)
        return qs


class SearchApiView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = (
            Job.objects.unfilled()
            .select_related("company", "user", "category")
            .prefetch_related("tags")
        )
        location = self.request.GET.get("location")
        position = self.request.GET.get("position")
        category = self.request.GET.get("category")
        if location:
            qs = qs.filter(location__icontains=location)
        if position:
            qs = qs.filter(title__icontains=position)
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=category)
            else:
                qs = qs.filter(category__slug=category)
        return qs
