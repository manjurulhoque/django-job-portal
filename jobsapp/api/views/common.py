from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ...models import Job
from ..serializers import JobSerializer


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    queryset = serializer_class.Meta.model.objects.unfilled()
    permission_classes = [AllowAny]


class SearchApiView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if "location" in self.request.GET and "position" in self.request.GET:
            return self.serializer_class.Meta.model.objects.unfilled(
                location__contains=self.request.GET["location"], title__contains=self.request.GET["position"]
            )
        else:
            return self.serializer_class.Meta.model.objects.unfilled()


@api_view(["GET"])
@permission_classes([AllowAny])
def categories_list_api_view(request):
    categories = [
        {"name": "Web design", "slug": "web-design", "icon": "lni-brush"},
        {"name": "Graphic design", "slug": "graphic-design", "icon": "lni-heart"},
        {"name": "Web development", "slug": "web-development", "icon": "lni-funnel"},
        {"name": "Human Resource", "slug": "human-resource", "icon": "lni-cup"},
        {"name": "Support", "slug": "support", "icon": "lni-home"},
        {"name": "Android Development", "slug": "android", "icon": "lni-world"},
    ]

    for category in categories:
        total_jobs = Job.objects.filter(category=category.get("slug")).count()
        category["total_jobs"] = total_jobs

    return JsonResponse(categories, safe=False)
