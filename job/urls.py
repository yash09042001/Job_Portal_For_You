from django.urls import path
from .views import JobCreateView
from .views import ActiveJobListView, ActiveJobDetaliView

app_name = 'job'

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='create_job'),
    path('active-job/', ActiveJobListView.as_view(), name='active_job_list'),
    path('<int:pk>', ActiveJobDetaliView.as_view(), name='active_job_detail'),
]
