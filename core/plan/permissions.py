from rest_framework.permissions import BasePermission


class IsCoachUser(BasePermission):
    '''Permission that checks if user is coach.'''
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_coach)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
