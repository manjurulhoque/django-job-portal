from rest_framework import viewsets, mixins, status
from .serializers import *


class JovViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = JobSerializer
    queryset = serializer_class.Meta.model.objects.all()
