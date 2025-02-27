from django.urls import path
from .api_views import JobListAPIView, JobDetailAPIView
from .api_views import JobCreateAPIView, JobUpdateAPIView, JobDeleteAPIView
from .api_views import JobListCandidatesAPIView, JobDetailCandidateAPIView
app_name = 'job_api'

urlpatterns = [
    path('joblist/', JobListAPIView.as_view(), name='joblist_api'),
    path('jobdetail/<int:pk>/', JobDetailAPIView.as_view(),
         name='jobdetailUpdate_api'),
    path('jobcreate/', JobCreateAPIView.as_view(),
         name='jobcreate_api'),
    path('jobupdate/<int:pk>/', JobUpdateAPIView.as_view(),
         name='jobupdate_api'),
    path('jobdelete/<int:pk>/', JobDeleteAPIView.as_view(),
         name='jobdelete_api'),


    path('c/joblist/', JobListCandidatesAPIView.as_view(),
         name='cjoblist_api'),
    path('c/jobdetail/<int:pk>/', JobDetailCandidateAPIView.as_view(),
         name='cjobdetail_api'),
]
