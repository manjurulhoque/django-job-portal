from django.urls import path

from .views import TagListAPIView

app_name = "tags-api"

urlpatterns = [path("tags/", TagListAPIView.as_view(), name="tag-list")]
