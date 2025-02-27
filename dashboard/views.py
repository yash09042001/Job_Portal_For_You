from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from application.models import Application
from job.models import Job


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboar View For The Candidate and Recruiter He/She login and Used"""
    template_name = 'dashboard/dashborad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # If the user is a recruiter
        if user.is_recruiter:
            # Get the count of created jobs for the recruiter
            context['job_count'] = Job.objects.filter(
                recruiter=user.recruiter).count()
            total_received_applications = Application.objects.filter(
                job__recruiter=user.recruiter).count()
            context[
                'total_received_applications'] = total_received_applications
            context['is_recruiter'] = True

        # If the user is a candidate
        elif user.is_candidate:
            # Get the counts for applications
            context['application_count'] = Application.objects.filter(
                candidate=user.candidate).count()
            context['in_process_count'] = Application.objects.filter(
                candidate=user.candidate, status='In Process').count()
            context['interview_scheduled_count'] = Application.objects.filter(
                candidate=user.candidate, status='Interview Scheduled').count()
            context['accepted_count'] = Application.objects.filter(
                candidate=user.candidate, status='Accepted').count()
            context['rejected_count'] = Application.objects.filter(
                candidate=user.candidate, status='Rejected').count()
            context['is_candidate'] = True

        return context
