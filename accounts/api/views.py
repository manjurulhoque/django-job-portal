from rest_framework import decorators, permissions, response, status
from rest_framework.request import Request

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from .serializers import UserCreateSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request: Request) -> response.Response:
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    serializer.save()
    res = {
        "status": True,
        "message": _("Successfully registered"),
    }
    return response.Response(res, status.HTTP_201_CREATED)
