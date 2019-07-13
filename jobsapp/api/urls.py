from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import JobViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet, base_name='jobs')

urlpatterns = []

urlpatterns += router.urls
