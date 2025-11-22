from rest_framework import permissions

class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.role == 'recruiter'
        return True
