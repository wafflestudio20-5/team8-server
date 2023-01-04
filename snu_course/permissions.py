from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsSafeOrAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsCreator(IsSafeOrAdminUser):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) or obj.created_by == request.user

    def has_permission(self, request, view):
        return True


class IsSafeOrAuthorizedUser(IsSafeOrAdminUser):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user != AnonymousUser

