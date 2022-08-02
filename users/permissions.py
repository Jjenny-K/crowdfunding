from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS 요청의 경우 허용
            return True

        return obj.email == request.user.email
