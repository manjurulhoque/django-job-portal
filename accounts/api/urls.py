from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .custom_claims import MyTokenObtainPairView
from .views import registration, EditEmployeeProfileAPIView

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view()),
    path("register/", registration, name="register"),
    path("login/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path(
        "employee/",
        include(
            [
                path(
                    "profile/",
                    EditEmployeeProfileAPIView.as_view(),
                    name="employee-profile",
                ),
            ]
        ),
    ),
]
