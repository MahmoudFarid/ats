from rest_framework import permissions


class BasePermission:
    def is_protected_request(self, request, view):
        return request.method in view.protected_methods


class HasCompanyPermission(permissions.BasePermission, BasePermission):
    def has_permission(self, request, view):
        if self.is_protected_request(request, view):
            user = request.user
            return hasattr(user, 'companyadmin')
        return True


class HasCompanyAdminPermission(permissions.BasePermission, BasePermission):
    def has_object_permission(self, request, view, obj):
        if self.is_protected_request(request, view):
            user = request.user
            return user.companyadmin.company == obj.company
        return True
