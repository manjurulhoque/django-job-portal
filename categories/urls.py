from django.urls import path

from .views import *

app_name = "categories"

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories-list"),
]
