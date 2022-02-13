from django.contrib.auth import get_user_model, login
from requests.exceptions import HTTPError
from rest_framework import decorators, permissions, response, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthForbidden, AuthTokenError, MissingBackend
from social_django.utils import load_backend, load_strategy

from jobsapp.api.permissions import IsEmployee

from .custom_claims import MyTokenObtainPairSerializer
from .serializers import SocialSerializer, UserCreateSerializer, UserSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    res = {"status": True, "message": "Successfully registered"}
    return response.Response(res, status.HTTP_201_CREATED)


class EditEmployeeProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ["get", "put"]
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_object(self):
        return self.request.user


class SocialLoginAPIView(GenericAPIView):
    """Log in using facebook"""

    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider", None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

        except MissingBackend:
            return Response({"error": "Please provide a valid provider"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get("access_token")
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response(
                {"error": {"access_token": "Invalid token", "details": str(error)}}, status=status.HTTP_400_BAD_REQUEST
            )
        except AuthTokenError as error:
            return Response({"error": "Invalid credentials", "details": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({"error": "invalid token", "details": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({"error": "invalid token", "details": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # generate JWT token
            login(request, authenticated_user)
            # data = {"token": jwt_encode_handler(jwt_payload_handler(user))}
            # token = RefreshToken.for_user(user)
            token = MyTokenObtainPairSerializer.get_token(user)
            # customized response
            context = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "access": str(token.access_token),
                "refresh": str(token),
            }
            return Response(status=status.HTTP_200_OK, data=context)
