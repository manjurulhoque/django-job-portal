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
