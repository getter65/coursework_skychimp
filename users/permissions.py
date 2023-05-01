from rest_framework import permissions


class UserChangeUserPermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(permissions__codename='change_user'):
            return True
        elif request.user == view.get_object():
            return True
        return False
