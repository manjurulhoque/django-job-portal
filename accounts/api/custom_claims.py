from typing import Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from ..models import User
from .serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # type: ignore
    @classmethod
    def get_token(cls, user: User) -> Any:
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["user"] = UserSerializer(user, many=False).data

        return token


class MyTokenObtainPairView(TokenObtainPairView):  # type: ignore
    serializer_class = MyTokenObtainPairSerializer
