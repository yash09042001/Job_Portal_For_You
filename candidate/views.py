from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from company.models import Company
from application.models import Application
from .forms import CandidateProfileForm
from .models import Candidate
from .models import User


class ProfileView(LoginRequiredMixin, DetailView):
    """Candidate Profile View When Candiate Login Show In Dashboard"""
    model = User
    template_name = 'candidate/cprofile.html'
    context_object_name = 'candidate'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class CandidateAppliedListView(LoginRequiredMixin, ListView):
    """Candidate Applied all Job Show In Dashboard"""
    model = Application
    template_name = 'candidate/my_applications.html'
    context_object_name = 'applications'

    """Candidate Applied all Job Filter In Dashboard"""
    def get_queryset(self):
        if not hasattr(self.request.user, 'candidate'):
            return Application.objects.none()

        queryset = Application.objects.filter(
            candidate=self.request.user.candidate).order_by('-created_at')

        # Apply filters
        title = self.request.GET.get('title')
        name = self.request.GET.get('company')
        status = self.request.GET.get('status')

        if title:
            queryset = queryset.filter(job__title__icontains=title)
        if name:
            queryset = queryset.filter(job__recruiter__company__name=name)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Preserve filters in the context
        context['title'] = self.request.GET.get('title', '')
        context['company_filter'] = self.request.GET.get('company', '')
        context['status_filter'] = self.request.GET.get('status', '')

        # Pass all companies and possible statuses to the template
        context['companies'] = Company.objects.all()
        # Assumes a choices field for status
        context['statuses'] = Application.STATUS_CHOICES
        return context


class CandidateProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Candidate Profile Update Any Wrong Info Than This View Work"""
    template_name = 'candidate/ceditprofile.html'
    # Replace with the actual name of the candidate profile view
    success_url = reverse_lazy('candidate:cprofile')

    def get(self, request, *args, **kwargs):
        """Handle GET requests to prefill the form with existing data."""
        user = request.user
        # Fetch the associated Candidate object
        candidate = get_object_or_404(Candidate, user=user)

        # Prefill the form with User and Candidate data
        form = CandidateProfileForm(instance=user)
        candidate_data = {
            'skill': candidate.skill,
            'experience': candidate.experience,
            'cv': candidate.cv,
            'portfolio': candidate.portfolio,
        }
        form.initial.update(candidate_data)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update User and Candidate data."""
        user = request.user
        candidate = get_object_or_404(Candidate, user=user)

        # Bind the form with POST data
        form = CandidateProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save User data
            user = form.save()

            # Update Candidate-specific fields
            candidate.skill = form.cleaned_data.get('skill')
            candidate.experience = form.cleaned_data.get('experience')
            candidate.cv = form.cleaned_data.get('cv')
            candidate.portfolio = form.cleaned_data.get('portfolio')
            candidate.save()

            messages.success(
                request, "Your profile has been updated successfully!")
            return redirect(self.success_url)

        messages.error(request, "Please fix the errors below.")
        return render(request, self.template_name, {'form': form})
