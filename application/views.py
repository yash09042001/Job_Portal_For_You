from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from .models import Application
from .forms import ApplicationCreationForm
from job.models import Job


class ApplicationCreateView(CreateView):
    """This Application Create View for Candiate his Used To Applied for Job"""
    model = Application
    form_class = ApplicationCreationForm
    template_name = 'application/apply.html'

    def form_valid(self, form):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        form.instance.job = job
        form.instance.candidate = self.request.user.candidate
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job:active_job_detail',
                            kwargs={'pk': self.kwargs['job_id']})
