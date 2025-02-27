from django.urls import path
from .views import ProfileView, RecruiterJobListView, RecruiterJobDetailView
from .views import ManageApplicationsView, RecruiterProfileUpdateView

app_name = 'recruiter'

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('recruiter_create_job', RecruiterJobListView.as_view(),
         name='recruiter_create_job'),
    path('<int:pk>', RecruiterJobDetailView.as_view(),
         name='recruiter_create_job_detail'),
    path('manage-applications/', ManageApplicationsView.as_view(),
         name='manage_applications'),
    path('edit', RecruiterProfileUpdateView.as_view(), name='reditprofile'),
]
