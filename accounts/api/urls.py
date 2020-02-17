from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .custom_claims import MyTokenObtainPairView

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view()),
    path('login/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
