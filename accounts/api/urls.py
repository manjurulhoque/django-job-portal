from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .custom_claims import MyTokenObtainPairView
from .views import EditEmployeeProfileAPIView, SocialLoginAPIView, registration

app_name = "accounts.api"

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view()),
    path("register/", registration, name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("employee/", include([path("profile/", EditEmployeeProfileAPIView.as_view(), name="employee-profile")])),
    path("oauth/login/", SocialLoginAPIView.as_view(), name="oauth-login"),
]
