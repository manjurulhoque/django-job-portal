import logging
from django.utils.translation import gettext_lazy as _

from utils.namedtuples import Checking

logger = logging.getLogger(__name__)


class BasePermission:
    message = None

    def has_permission(self, request, **kwargs):
        return True

    def has_object_permission(self, request, obj, **kwargs):
        return True

    def set_message_and_get_checking_status(self, checking: Checking, message=None) -> bool:
        self.message = message or checking.message
        return checking.passed


class AllowAny(BasePermission):
    def has_permission(self, request, **kwargs):
        return True


class IsAuthenticated(BasePermission):
    message = _("Unauthenticated request.")

    def has_permission(self, request, **kwargs):
        return bool(request.user and request.user.is_authenticated)


class IsEmployer(BasePermission):
    message = _("Your user account must be an employer")

    def has_permission(self, request, **kwargs):
        return bool(request.user and request.user.role == "employer")


class IsEmployee(BasePermission):
    message = _("Your user account must be an employee")

    def has_permission(self, request, **kwargs):
        return bool(request.user and request.user.role == "employee")
