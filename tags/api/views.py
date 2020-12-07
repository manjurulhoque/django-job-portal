from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from tags.api.serializers import TagSerializer


class TagListAPIView(ListAPIView):
    serializer_class = TagSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = [AllowAny]
