from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from jobsapp.api.serializers import JobSerializer
from jobsapp.models import Job


class JobPagination(PageNumberPagination):
    page_size = 9


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.unfilled().select_related("company", "user").prefetch_related("tags")
    permission_classes = [AllowAny]
    pagination_class = JobPagination


class SearchApiView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Job.objects.unfilled().select_related("company", "user").prefetch_related("tags")
        if "location" in self.request.GET and "position" in self.request.GET:
            return qs.filter(
                location__contains=self.request.GET["location"],
                title__contains=self.request.GET["position"],
            )
        return qs
