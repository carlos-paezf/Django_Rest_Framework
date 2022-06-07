# User Endpoint

## Test

Vamos al archivo `user/tests/test_user_api.py` y creamos una url para el usuario autenticado. Luego verificamos que en la autenticación sera requerida para el usuario desde la url pública. Creamos una clase para la parte privada de la api, en la cuál probamos que el usuario hace login perfectamente, que no pueda ejecutar el método POST en ningún caso, y por último, que pueda actualizar su perfil mediante el método PATCH.

```py
...
ME_URL = reverse('user:me')
...

class PublicUserAPITests(TestCase):
    ...
    def test_retrieve_user_unauthorize(self):
        """ > Probar que la autenticación sea requerida para los usuarios """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """ > Probar el API privado del usuario """

    def setUp(self):
        self.user = createUser(email='test@test.com', password='test_123', name='test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ > Probar obtener perfil para usuario con login """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ > Probar que el POST no sea permitido """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ > Probar que el usuario está siendo actualizado si está autenticado """
        payload = {
            'password': 'updated_123',
            'name': 'update'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
```

## Vista

Creamos una nueva clase para poder manejar la vista del usuario, es importante importar los paquetes `authentication` y `permissions` para clases de autenticación y permisos.

```py
from rest_framework import generics, authentication, permissions
...

class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manejar el usuario autenticado """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """ Obtener y retornar usuario autenticado """
        return self.request.user
```

Dentro del serializador del usuario en el archivo `user/serializers.py`, añadimos una nueva función para el momento de actualizar el user:

```py
class UserSerializer(serializers.ModelSerializer):
    ...
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
```

Por último registramos la vista dentro de `user/urls.py`:

```py
urlpatterns = [
    ...,
    path('me/', views.ManageUserView.as_view(), name='me')
]
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Token API](12_Token_API.md) | [Readme](../../README.md) | [App para Recetas](14_App_Recetas.md) |
