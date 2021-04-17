from rest_framework.permissions import BasePermission

from jobsapp.models import Job


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "employer"


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "employee"


class IsJobCreator(BasePermission):
    # message = 'Permission denied'

    def has_permission(self, request, view):
        job_id = view.kwargs.get("job_id")
        if job_id:
            if Job.objects.filter(id=job_id, user=request.user).exists():
                return True
            else:
                return False
        return False


# collected from https://stackoverflow.com/a/58100813/5559590
class IsAuthenticatedOrClientCredentialPermission(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        grant_type = request.auth.application.get_authorization_grant_type_display()
        if request.user is None:
            if grant_type == 'Client credentials':
                request.user = request.auth.application.user  # <-- this is because I needed to get the user either the grant is 'password' or 'client credentials'
                return True
            else:
                return False
        else:
            return True


class ClientCredentialPermission(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        grant_type = request.auth.application.get_authorization_grant_type_display()
        if request.user is None and grant_type == 'Client credentials':
            return True
        else:
            return False
