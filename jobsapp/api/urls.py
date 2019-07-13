from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import JovViewSet

router = DefaultRouter()
router.register('jobs', JovViewSet, base_name='jobs')

urlpatterns = []

urlpatterns += router.urls
