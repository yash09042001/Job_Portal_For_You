from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):
    """
    Custom permission to allow access only to authenticated recruiters.
    """

    def has_permission(self, request, view):
        # User must be authenticated and associated with a Recruiter
        return bool(request.user.is_authenticated and hasattr(
            request.user, 'recruiter'))

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to ensure only the recruiter who created
        the job can access it.
        """
        try:
            recruiter = request.user.recruiter
        except AttributeError:
            return False

        return obj.recruiter == recruiter
