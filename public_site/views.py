from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from job.models import Job


class JobListView(ListView):
    model = Job
    template_name = 'public_site/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.all().order_by('-created_at')


class JobDetailView(DetailView):
    model = Job
    template_name = 'public_site/job_detail.html'
    context_object_name = 'job'


class HomeView(TemplateView):
    template_name = 'public_site/home.html'
