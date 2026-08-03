from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from accounts.models import User
from categories.models import Category
from ..decorators import user_is_employee
from ..forms import ApplyJobForm
from ..models import Applicant, Company, Favorite, Job


class HomeView(ListView):
    model = Job
    template_name = "home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.unfilled().select_related("company", "category")[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trendings"] = self.model.objects.unfilled(
            created_at__month=timezone.now().month
        ).select_related("company", "category")[:3]
        context["live_jobs_count"] = self.model.objects.unfilled().count()
        context["companies_count"] = Company.objects.count()
        context["candidates_count"] = User.objects.filter(role="employee").count()
        context["new_jobs_count"] = self.model.objects.unfilled(created_at__month=timezone.now().month).count()
        return context


class AboutUsView(TemplateView):
    template_name = "about_us.html"


class SearchView(ListView):
    model = Job
    template_name = "jobs/search.html"
    context_object_name = "jobs"

    def get_queryset(self):
        qs = self.model.objects.unfilled().select_related("company", "category").prefetch_related("tags")
        location = self.request.GET.get("location", "")
        position = self.request.GET.get("position", "")
        category = self.request.GET.get("category", "")
        if location:
            qs = qs.filter(location__icontains=location)
        if position:
            qs = qs.filter(title__icontains=position)
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("name")
        return context


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self):
        qs = self.model.objects.unfilled().select_related("company", "category").prefetch_related("tags").order_by("-created_at")
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["total_jobs"] = self.get_queryset().count()
        data["categories"] = Category.objects.all().order_by("name")
        return data


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobs/details.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = "job_id"
    slug_url_kwarg = "job_id"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self._allowed_methods())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, "Successfully applied for the job!")
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy("jobs:home"))

    def get_success_url(self):
        return reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs["job_id"])
        if applicant:
            messages.info(self.request, "You already applied for this job")
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


def favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={"auth": False, "status": "error"})

    job_id = request.POST.get("job_id")
    user_id = request.user.id
    try:
        fav = Favorite.objects.get(job_id=job_id, user_id=user_id, soft_deleted=False)
        if fav:
            fav.soft_deleted = True
            fav.save()
            return JsonResponse(
                data={"auth": True, "status": "removed", "message": "Job removed from your favorite list"}
            )
    except Favorite.DoesNotExist:
        Favorite.objects.create(job_id=job_id, user_id=user_id)
        return JsonResponse(data={"auth": True, "status": "added", "message": "Job added to your favorite list"})
