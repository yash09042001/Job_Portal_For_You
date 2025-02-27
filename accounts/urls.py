from django.urls import path
from .views import RecruiterRegistrationView, CandidateRegistrationView
from .views import UserLoginView
from .views import logout_view

app_name = 'accounts'

urlpatterns = [
    path('recruiter_register',
         RecruiterRegistrationView.as_view(), name='recruiter_register'),
    path('candidate_register',
         CandidateRegistrationView.as_view(), name='candidate_register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
