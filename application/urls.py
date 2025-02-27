from django.urls import path
from .views import ApplicationCreateView

app_name = 'application'

urlpatterns = [
    path('apply/<int:job_id>/', ApplicationCreateView.as_view(),
         name='apply_job'),
]
