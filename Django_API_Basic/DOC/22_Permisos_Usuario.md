# Permisos de Usuario

Tenemos el problema de que cualquier usuario puede crear un registro, por lo tanto vamos a evitar este incidente mediante permisos de usuario. Dentro de `profiles_api` creamos un nuevo archivo llamado `permissions.py`, el cuál contendrá la siguiente información: Una clase que hereda de `BasePermission` de `rest_framework`, y dentro de nuestra clase definimos el método para saber si el usuario puede editar su propio perfil.

```py
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, object):
        if request.method in permission.SAFE_METHODS:
            return true

        return object.id == request.user.id
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Crear perfiles ViewSet](21_Crear_Perfiles_ViewSet.md) | [Readme](../../README.md) | [Autenticación y Permisos de ViewSet](23_Autenticacion_Permisos_ViewSet.md) |
