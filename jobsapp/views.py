from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from jobsapp.forms import CreateJobForm
from jobsapp.models import Job


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        print(request.POST['type'])
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
