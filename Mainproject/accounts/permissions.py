from rest_framework import permissions

class IsRecruiterOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'recruiter_profile') and obj.recruiter == request.user.recruiter_profile
