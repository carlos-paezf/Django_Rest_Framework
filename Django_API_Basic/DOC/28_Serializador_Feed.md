# Serializador del Feed

Creamos un serializador para nuestro modelo, por lo que vamos al archivo `profile_api/serializers.py` y creamos una nueva clase, en la creamos la relación con el modelo a serializar, y los campos que tiene dicho modelo. Por último definimos que el campo de `user_profile` será de solo lectura:

```py
class ProfileFeedItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
```

## ViewSet para Feed de Usuario

Creamos un ViewSet para el Feed de Usuarios dentro del archivo `profile_api/views.py`:

```py
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializers
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_profile = self.request.user)
```

Luego, dentro de `profile_api/urls.py`, registramos nuestro ViewSet:

```py
...
router.register('feed', views.UserProfileFeedViewSet)
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Agregando Ítem de modelo](27_Agregando_Item_Modelo.md) | [Readme](../../README.md) | [Editando permiso del API](29_Editando_Permisos_API.md) |
