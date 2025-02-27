from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .forms import RecruiterRegistrationForm, CandidateRegistrationForm
from .models import User


class RecruiterRegistrationView(CreateView):
    model = User
    form_class = RecruiterRegistrationForm
    template_name = 'accounts/recruiter_register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_recruiter = True  # Assuming this is how you flag a recruiter
        user.save()
        form.save_m2m()  # Save many-to-many relationships, if any
        return super().form_valid(form)


class CandidateRegistrationView(CreateView):
    model = User
    form_class = CandidateRegistrationForm
    template_name = 'accounts/candidate_register.html'
    success_url = reverse_lazy('accounts:login')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('public_site:home'))
