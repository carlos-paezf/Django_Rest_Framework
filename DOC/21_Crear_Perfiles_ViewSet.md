# Crear perfiles ViewSet

Vamos a importar nuestro modelos dentro del archivo `profiles_api/views.py`, junto a la importación de los serializers:

```py
from profiles_api import serializers, models
```

Definimos una clase que va a heredar de `ModelViewSet`, la cual nos permite crear los ViewSets a partir de modelos. Creamos un serializador basado en nuestra clase `UserProfileSerializer` dentro del módulo de serializers. También tenemos una consulta en la que obtenemos todos los objetos creados para el modelo de `UserProfile`:

```py
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializers
    query_set = models.UserProfile.objects.all()
```

Debemos registrar nuestro ViewSet, por lo que vamos al archivo `profiles_api/urls.py` y lo agregamos de la siguiente manera:

```py
router.register('profile', views.UserProfileViewSet)
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Actualización de Contraseña y Login de Usuario](20_Actualización_Password_Login_Usuario.md) | [Readme](../README.md) | [Perfil de Usuario con API](22_Perfil_Usuario_API.md) |
