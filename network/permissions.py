from rest_framework.permissions import BasePermission

class IsActiveStaff(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.is_staff and u.is_active)
