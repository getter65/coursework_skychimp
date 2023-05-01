from rest_framework import permissions


class UserChangeLessonPermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(permissions__codename='change_lesson'):
            return True
        elif request.user == view.get_object().author:
            return True
        return False


class UserRetrieveLessonPermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(permissions__codename='view_lesson'):
            return True
        elif request.user == view.get_object().author:
            return True
        return False


class UserChangeCoursePermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(permissions__codename='change_course'):
            return True
        elif request.user == view.get_object().author:
            return True
        return False


class UserRetrieveCoursePermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(permissions__codename='view_course'):
            return True
        elif request.user == view.get_object().author:
            return True
        return False
