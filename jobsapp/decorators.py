from django.core.exceptions import PermissionDenied


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == "employer":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == "employee":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
