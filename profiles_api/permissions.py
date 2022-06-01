from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Permitir al usuario editar su propio perfil """

    def has_object_permission(self, request, view, object):
        """ Consultar si un usuario está tratando de editar su propio perfil """
        if request.method in permission.SAFE_METHODS:
            return true

        return object.id == request.user.id
