from django.urls import path
from .views import ProfileView, CandidateAppliedListView
from .views import CandidateProfileUpdateView

app_name = 'candidate'

urlpatterns = [
    path('profile', ProfileView.as_view(), name='cprofile'),
    path('my_application', CandidateAppliedListView.as_view(),
         name='my_applications'),
    path('edit', CandidateProfileUpdateView.as_view(), name='ceditprofile'),
]
