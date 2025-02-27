from rest_framework.generics import ListAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import JobSerializers, JobPartialUpdateSerializer
from rest_framework.exceptions import PermissionDenied, NotFound
from recruiter.models import Recruiter
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from django.utils.timezone import now
from accounts.permissions import IsRecruiter


@extend_schema_view(
    get=extend_schema
    (description="Retrieve a list of jobscreated by the logged-in recruiter."),
)
class JobListAPIView(ListAPIView):
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        """
        Override to return only the jobs created by the logged-in recruiter.
        """
        try:
            # Retrieve the Recruiter instance for the logged-in user
            recruiter = self.request.user.recruiter
        except AttributeError:
            return Job.objects.none()
        return Job.objects.filter(recruiter=recruiter)


@extend_schema_view(
    get=extend_schema
    (description="details of specific job created by logged-in recruiter"),
)
class JobDetailAPIView(RetrieveAPIView):
    serializer_class = JobSerializers

    def get_queryset(self):
        """
        Override to ensure that only the jobs created by the
        logged-in recruiter are returned.
        """
        if hasattr(self.request.user, 'recruiter'):
            recruiter = self.request.user.recruiter
            return Job.objects.filter(recruiter=recruiter)
        else:
            raise PermissionDenied("Only recruiters can view job details.")


@extend_schema_view(
    post=extend_schema
    (description="Create new job.Only accessible to authenticated recruiters"),
)
class JobCreateAPIView(CreateAPIView):
    serializer_class = JobSerializers
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def perform_create(self, serializer):
        # Check if the user is associated with a recruiter profile
        if not hasattr(self.request.user, 'recruiter'):
            raise PermissionError("Only recruiters can create jobs.")

        try:
            # Get the Recruiter instance associated with the user
            recruiter = Recruiter.objects.get(user=self.request.user)
        except Recruiter.DoesNotExist:
            raise PermissionError(
                "The user is not associated with a recruiter profile.")

        # Save the job with the recruiter instance
        serializer.save(recruiter=recruiter)

    def post(self, request, *args, **kwargs):
        # Check if the user has a recruiter profile
        if not hasattr(request.user, 'recruiter'):
            return Response(
                {"error": "Candidates can't access this page."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema
    (description="specific job created by the logged-in recruiter."),
    patch=extend_schema
    (description="Partially update `deadlines` and `status` of a job.")
)
class JobUpdateAPIView(RetrieveAPIView, UpdateAPIView):
    serializer_class = JobPartialUpdateSerializer
    queryset = Job.objects.all()

    def get_queryset(self):
        """
        Override to return only the jobs created by the logged-in recruiter.
        """
        if hasattr(self.request.user, 'recruiter'):
            recruiter = self.request.user.recruiter
            return Job.objects.filter(recruiter=recruiter)
        else:
            raise PermissionDenied("Only recruiters can update job details.")

    def perform_update(self, serializer):
        """
        Ensure that the logged-in recruiter can only
        update the job they created.
        """
        job = self.get_object()
        if job.recruiter != self.request.user.recruiter:
            return Response(
                {"error": "You do not have permission to update this job."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH request for updating the job's `deadline` and `status`.
        """
        return self.update(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema
    (description="details of specific job created by the logged-in recruiter"),
    delete=extend_schema
    (description="Delete a specific job created by the logged-in recruiter.")
)
class JobDeleteAPIView(RetrieveAPIView, DestroyAPIView):
    """
    This view allows a recruiter to delete a job they created.
    Only the recruiter who created the job can delete it.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit the queryset to only jobs created by the logged-in recruiter.
        If the job doesn't belong to the logged-in recruiter,
        it won't be available.
        """
        # Get the recruiter instance
        if hasattr(self.request.user, 'recruiter'):
            recruiter = self.request.user.recruiter
            return Job.objects.filter(recruiter=recruiter)
        else:
            raise PermissionDenied("Only recruiters can delete jobs.")

    def perform_destroy(self, instance):
        """
        Ensure that the logged-in recruiter is the owner of the job before
        deleting. If the job doesn't exist or doesn't belong to the logged-in
          recruiter, return an error.
        """
        if instance.recruiter != self.request.user.recruiter:
            raise PermissionDenied(
                "You do not have permission to delete this job.")

        """If job is not found or belongs to another recruiter,
          raise NotFound exception"""
        if not instance:
            raise NotFound("Job not available or doesn't exist.")

        instance.delete()
        return Response(
            {"message": "Job deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


@extend_schema_view(
    get=extend_schema
    (description="Retrieve a list of job for by the logged-in candidate."),
)
class JobListCandidatesAPIView(ListAPIView):
    """
    API to list all recruiter-created jobs for logged-in candidates.
    """
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Restrict recruiters from accessing the job list view.
        """
        if hasattr(request.user, 'recruiter'):
            raise PermissionDenied(
                "Recruiters cannot access the candidate job list.")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return all open jobs posted by recruiters for candidates.
        """
        if hasattr(self.request.user, 'candidate'):
            return Job.objects.filter(
                status='open', deadlines__gte=now()).order_by('deadlines')
        raise PermissionDenied("Only candidates can view the job list.")

    def get_serializer_context(self):
        """
        Pass the request to the serializer for custom field logic.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema_view(
    get=extend_schema
    (description="Retrieve details of specific job for logged in candidate"),
)
class JobDetailCandidateAPIView(RetrieveAPIView):
    """
    API to show the detailed job information for candidates,
    only for open jobs.
    """
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Restrict recruiters from accessing the job detail view.
        """
        if hasattr(request.user, 'recruiter'):
            raise PermissionDenied(
                "Recruiters cannot access the candidate job details.")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter jobs to ensure only open jobs are accessible.
        """
        if hasattr(self.request.user, 'candidate'):
            return Job.objects.filter(status='open',
                                      deadlines__gte=now().date())
        raise PermissionDenied("Only candidates can access job details.")

    def get_object(self):
        """
        Ensure that the job object exists and meets the criteria.
        """
        job = super().get_object()
        current_date = now().date()  # Get the current date
        if job.status != 'open' or job.deadlines < current_date:
            raise NotFound("This job is no longer available.")
        return job

    def get_serializer_context(self):
        """
        Pass the request to the serializer for custom field logic.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
