from rest_framework import permissions


class IsCompanyStaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'companystaff')
