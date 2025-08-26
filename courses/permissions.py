from rest_framework import permissions


# class IsModeratorNoCreateDelete(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         user = request.user
#         if not user or not user.is_authenticated:
#             return False
#
#         is_moderator = user.groups.filter(name='moderators').exists()
#         if not is_moderator:
#             return False
#
#         if request.method in ['POST', 'DELETE']:
#             return False
#         return True

class IsModeratorOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True

        return obj.owner == request.user