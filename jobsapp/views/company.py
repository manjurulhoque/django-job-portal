from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CompanyForm
from jobsapp.models import Company, Job


class CompanyListView(ListView):
    model = Company
    template_name = "jobs/company/list.html"
    context_object_name = "companies"
    paginate_by = 12

    def get_queryset(self):
        queryset = Company.objects.all()
        # Filter by industry if provided
        industry = self.request.GET.get("industry", "")
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        return queryset


class FeaturedCompanyListView(ListView):
    model = Company
    template_name = "jobs/company/featured.html"
    context_object_name = "companies"
    paginate_by = 12

    def get_queryset(self):
        return Company.objects.filter(featured=True)


class CompanyDetailView(DetailView):
    model = Company
    template_name = "jobs/company/detail.html"
    context_object_name = "company"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all active jobs for this company
        context["jobs"] = Job.objects.filter(company=self.object, filled=False).order_by("-created_at")
        context["total_jobs"] = context["jobs"].count()
        return context

    def get_object(self, queryset=None):
        obj = super(CompanyDetailView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Company doesn't exist")
        return obj


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class CompanyCreateView(CreateView):
    template_name = "jobs/company/create.html"
    form_class = CompanyForm
    extra_context = {"title": "Create Company Profile"}
    success_url = reverse_lazy("jobs:company-list")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("accounts:login")
        if self.request.user.is_authenticated and self.request.user.role != "employer":
            return reverse_lazy("accounts:login")
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Company profile created successfully!")
        return super(CompanyCreateView, self).form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class CompanyUpdateView(UpdateView):
    template_name = "jobs/company/update.html"
    form_class = CompanyForm
    extra_context = {"title": "Edit Company Profile"}
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("jobs:company-list")
    context_object_name = "company"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # Only allow users to edit their own companies
        return Company.objects.filter(user_id=self.request.user.id)

    def form_valid(self, form):
        messages.success(self.request, "Company profile updated successfully!")
        return super(CompanyUpdateView, self).form_valid(form)

