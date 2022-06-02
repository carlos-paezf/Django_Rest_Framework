# Editando permiso del API

Vamos a editar los permisos para editar el feed, por lo que vamos al archivo `profile_api/permissions.py` y creamos un nuevo permiso:

```py
class UpdateOwnStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.user_profile_id == request.user.id
```

Dentro del archivo `profile_api/views.py` importamos la clase `IsAuthenticatedOrReadOnly` de `rest_framework` en su módulo `permissions` para que en caso de que los usuarios no estén autenticados, puedan leer la información. En caso de que querer proteger la información, podemos importar la clase `IsAuthenticated`. Luego dentro del ViewSet `UserProfileFeedViewSet` añadimos una tupla de permisos:

```py
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticatedOrReadOnly)
    ...
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Serializador del Feed](28_Serializador_Feed.md) | [Readme](../README.md) |  |
