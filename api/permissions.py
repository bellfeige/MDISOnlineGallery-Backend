from rest_framework import permissions


# from .models import


class IsDigitalArtOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user and request.user.is_designer == True) \
               or request.user.is_superuser == True

    def has_permission(self, request, view):
        return request.user.is_superuser == True or request.user.is_designer == True


class IsAdminAndOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser == True

    def has_permission(self, request, view):
        return request.user.is_superuser == True


class IsCurrentUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_superuser == True

    # def has_permission(self, request, view):
    #     return request.user.is_superuser == True


class IsMyCartOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id or request.user.is_superuser == True

    # def has_permission(self, request, view):
    #     return request.user.is_member == True \
    #            or request.user.is_designer == True \
    #            or request.user.is_superuser == True
