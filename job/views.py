from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from application.models import Application
from company.models import Company
from .models import Job
from .forms import JobCreationForm
from django.utils.timezone import now


class JobCreateView(LoginRequiredMixin, CreateView):
    """Job Cerate For The Recruiter He/She Create A Job Based On Requirement"""
    model = Job
    form_class = JobCreationForm
    template_name = 'job/create_job.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_queryset(self):
        return Job.objects.all().order_by('-created_at')

    def form_valid(self, form):
        # Ensure created_at is set
        if not self.object:
            form.instance.created_at = now()
        form.instance.recruiter = self.request.user.recruiter
        return super().form_valid(form)


class ActiveJobListView(LoginRequiredMixin, ListView):
    """Active Job List View Show Active Job To The Candidate"""
    model = Job
    template_name = 'job/active_job_list.html'
    context_object_name = 'jobs'

    """Filter For Candidate Can Filter Job/Company Using Title/name """
    def get_queryset(self):
        queryset = Job.objects.filter(
            status='open', deadlines__gte=now().date()).order_by('-created_at')

        # Handle filters
        title = self.request.GET.get('title')
        name = self.request.GET.get('company')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if name:
            queryset = queryset.filter(recruiter__company__name=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = self.request.user.candidate  # Get the logged-in candidate
        applied_jobs = Application.objects.filter(candidate=candidate)

        # Add applied job IDs to context
        context['applied_job_ids'] = applied_jobs.values_list('job_id',
                                                              flat=True)

        # Preserve current filters in the context
        context['title'] = self.request.GET.get('title', '')
        context['company_filter'] = self.request.GET.get('company', '')

        # Pass all companies for the dropdown
        context['companies'] = Company.objects.all()

        return context


class ActiveJobDetaliView(LoginRequiredMixin, DetailView):
    """Active Job Detail Show To The Candidate"""
    model = Job
    template_name = 'job/active_job_detail.html'
    context_object_name = 'job'
