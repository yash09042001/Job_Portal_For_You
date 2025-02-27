from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from job.models import Job
from django.contrib import messages
from application.models import Application
from .models import User
from .models import Recruiter
from .forms import RecruiterProfileForm


class ProfileView(LoginRequiredMixin, DetailView):
    """Recruiter Profil View"""
    model = User
    template_name = 'recruiter/profile.html'
    context_object_name = 'recruiter'

    def get_object(self):
        # Get the user profile of the logged-in user
        return get_object_or_404(User, pk=self.request.user.pk)


class RecruiterJobListView(LoginRequiredMixin, ListView):
    """Lists all the jobs created by the logged-in recruiter."""
    model = Job
    template_name = 'recruiter/recruiter_create_job.html'
    context_object_name = 'jobs'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'recruiter'):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(
            recruiter=self.request.user.recruiter).order_by('-created_at')


class RecruiterJobDetailView(LoginRequiredMixin, DetailView):
    """Recruiter Create a job This Time Detail Info About Job"""
    model = Job
    template_name = 'recruiter/recruiter_create_job_detail.html'


class ManageApplicationsView(LoginRequiredMixin, ListView):
    """Recruiter Manage Applications for Jobs Created by Them"""
    model = Application
    template_name = 'recruiter/manage_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Ensure the user is a recruiter
        if not hasattr(self.request.user, 'recruiter'):
            return Application.objects.none()

        recruiter = self.request.user.recruiter
        jobs = Job.objects.filter(recruiter=recruiter)

        # Start with all applications for jobs created by the recruiter
        queryset = Application.objects.filter(
            job__in=jobs).order_by('created_at')

        # Apply filter by job title if provided
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(job__title__icontains=title)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add context for filter options
        context['jobs'] = Job.objects.filter(
            recruiter=self.request.user.recruiter)
        context['job_filter'] = self.request.GET.get('title', '')
        return context


class RecruiterProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Recruiter Profil Update View"""
    template_name = 'recruiter/reditprofile.html'
    success_url = reverse_lazy('recruiter:profile')

    def get(self, request, *args, **kwargs):
        """Handle GET requests to prefill the form with existing data."""
        user = request.user
        recruiter = get_object_or_404(Recruiter, user=user)

        # Prefill the form with User and Recruiter data
        form = RecruiterProfileForm(instance=user)
        recruiter_data = {
            'company': recruiter.company,
            'job_title': recruiter.job_title,
            'contact_email': recruiter.contact_email,
            'contact_number': recruiter.contact_number,
        }
        form.initial.update(recruiter_data)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update User and Recruiter data."""
        user = request.user
        recruiter = get_object_or_404(Recruiter, user=user)

        # Bind the form with POST data
        form = RecruiterProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save User data
            user = form.save()

            # Update Recruiter-specific fields
            recruiter.company = form.cleaned_data.get('company')
            recruiter.job_title = form.cleaned_data.get('job_title')
            recruiter.contact_email = form.cleaned_data.get('contact_email')
            recruiter.contact_no = form.cleaned_data.get('contact_number')
            recruiter.save()

            messages.success(request,
                             "Your profile has been updated successfully!")
            return redirect(self.success_url)

        messages.error(request, "Please fix the errors below.")
        return render(request, self.template_name, {'form': form})
