from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .custom_claims import MyTokenObtainPairView
from .views import EditEmployeeProfileAPIView, SocialLoginAPIView, registration

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view()),
    path("register/", registration, name="register"),
    path("login/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("employee/", include([path("profile/", EditEmployeeProfileAPIView.as_view(), name="employee-profile")])),
    path("oauth/login/", SocialLoginAPIView.as_view()),
]
