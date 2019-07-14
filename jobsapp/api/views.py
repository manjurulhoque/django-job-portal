from rest_framework import viewsets, mixins, status

from .serializers import *
from rest_framework.generics import ListAPIView


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    queryset = serializer_class.Meta.model.objects.all()


class SearchView(ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(location__contains=self.request.GET['location'],
                                                               title__contains=self.request.GET['position'])
