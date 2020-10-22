from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from django.views import View


class IsEmployer(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user and request.user.role == "employer"


class IsEmployee(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user and request.user.role == "employee"
