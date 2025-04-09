from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
