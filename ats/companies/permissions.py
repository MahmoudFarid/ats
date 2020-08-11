from rest_framework import permissions


class BasicPermission:
    def get_allowed_methods(self, view):
        default = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if view.allowed_methods:
            return view.allowed_methods
        return default


class IsCompanyStaffPermission(permissions.BasePermission, BasicPermission):

    def has_permission(self, request, view):
        allowed_methods = self.get_allowed_methods(view)
        if request.method in allowed_methods:
            user = request.user
            return hasattr(user, 'companystaff')
        return True


class CompanyOwnerRequired(permissions.BasePermission, BasicPermission):

    def has_object_permission(self, request, view, obj):
        allowed_methods = self.get_allowed_methods(view)
        if request.method in allowed_methods:
            user = request.user.companystaff
            return obj.created_by == user
        return True
