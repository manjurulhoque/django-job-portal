from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employee
from jobsapp.models import Applicant, Favorite


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employee, name="dispatch")
class EmployeeMyJobsListView(ListView):
    model = Applicant
    template_name = "jobs/employee/my-applications.html"
    context_object_name = "applicants"
    paginate_by = 6

    def get_queryset(self):
        self.queryset = (
            self.model.objects.select_related("job").filter(user_id=self.request.user.id).order_by("-created_at")
        )
        if (
            "status" in self.request.GET
            and len(self.request.GET.get("status")) > 0
            and int(self.request.GET.get("status")) > 0
        ):
            self.queryset = self.queryset.filter(status=int(self.request.GET.get("status")))
        return self.queryset


class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = "employee"
    template_name = "jobs/employee/edit-profile.html"
    success_url = reverse_lazy("accounts:employee-profile-update")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employee, name="dispatch")
class FavoriteListView(ListView):
    model = Favorite
    template_name = "jobs/employee/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return self.model.objects.select_related("job__user").filter(soft_deleted=False, user=self.request.user)
