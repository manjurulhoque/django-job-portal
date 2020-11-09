from django.contrib.auth import get_user_model
from rest_framework import response, decorators, permissions, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from jobsapp.api.permissions import IsEmployee
from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    res = {
        "status": True,
        "message": 'Successfully registered',
    }
    return response.Response(res, status.HTTP_201_CREATED)


class EditEmployeeProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_object(self):
        return self.request.user
