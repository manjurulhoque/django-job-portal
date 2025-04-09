from rest_framework import serializers

from ..models import *


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs["partial"] = True
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password", "user_permissions", "groups", "is_staff", "is_active", "is_superuser", "last_login")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = ["email", "password", "password2", "gender", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Email addresses must be unique."})
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        gender = validated_data["gender"]
        role = validated_data["role"]
        user = User(email=email, gender=gender, role=role)
        user.set_password(password)
        user.save()
        return user


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
