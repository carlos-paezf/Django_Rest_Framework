# Autenticación y Permisos de ViewSet

Dentro del archivo `profiles/views.py` importamos una clase llamada `TokenAuthentication`, el cual funciona generando un random token string cada que el usuario se logea. También importamos nuestro archivo de permisos:

```py
from rest_framework.authentication import TokenAuthentication 
```

Luego dentro de nuestra clase `UserProfileViewSet` creamos 2 atributos. En el primero almacenamos una lista con las clases de autenticación, y el segundo tenemos una lista con las clases de permisos:

```py
class UserProfileViewSet(viewsets.ModelViewSet):
    ...
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
```

Cuando ingresamos al endpoint `http://127.0.0.1:8000/api/profile/<id-usuario>`, si nuestro id de usuario coincide con el del parámetro, podemos editar la información, en caso contrario solo la podemos observar.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Permisos de Usuario](22_Permisos_Usuario.md) | [Readme](../README.md) | [Filtrar Usuarios](24_Filtrar_Usuarios.md) |
