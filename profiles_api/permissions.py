from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Permitir al usuario editar su propio perfil """

    def has_object_permission(self, request, view, object):
        """ Consultar si un usuario está tratando de editar su propio perfil """
        if request.method in permission.SAFE_METHODS:
            return true

        return object.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """ Permitir que el usuario actualice su propio Status Update """
    def has_object_permission(self, request, view, object):
        """ Consultar si un usuario está tratando de editar su propio perfil """
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.user_profile_id == request.user.id
