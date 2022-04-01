from django.contrib.auth.mixins import AccessMixin


class EmployeeRequiredMixin(AccessMixin):
    """Verify that the current user is employee."""

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.role != "employee":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class EmployerRequiredMixin(AccessMixin):
    """Verify that the current user is employee."""

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.role != "employer":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)