from django.urls import path
from .views import JobListView, JobDetailView, HomeView

app_name = 'public_site'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('job', JobListView.as_view(), name='job_list'),
    path('<int:pk>', JobDetailView.as_view(), name='job_detail'),
]
