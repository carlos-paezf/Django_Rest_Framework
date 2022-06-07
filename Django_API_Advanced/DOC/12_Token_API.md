# Token API

## Test

Vamos a crear 4 tests: Uno para verificar que el token se creo correctamente, otro en caso de dar credenciales invalidas, otro para autenticación de un usuario no existente, y un último para verificar que pasa cuando se hace un request que no incluye una contraseña. Dichos test los vamos a realizar dentro del archivo `user/tests/test_user_api.py`:

```py
...
TOKEN_URL = reverse('user:token')
...

class PublicUserAPITests(TestCase):
    ...
    def test_create_token_for_user(self):
        """ > Probar que el token será creado para el usuario """
        payload = {
            'email': 'test@test.com',
            'password': 'test_123',
            'name': 'Test name'
        }
        createUser(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ > Probar que el token no es creado con credenciales invalidas """
        createUser(email='test@test.com', password='testpass')
        payload = {
            'email': 'test@test.com',
            'password': 'testwrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ > Probar que no se creó el token si no existe el usuario """
        payload = {
            'email': 'test@test.com',
            'password': 'testwrong',
            'name': 'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ > Probar que el email y la contraseña sean requeridas """
        res = self.client.post(TOKEN_URL, { 'email': 'one', 'password': '' })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

## Serializador

Lo primero será crear un serializador, por lo que nos dirigimos a `user/serializers.py` y añadimos el siguiente código: Importamos la función `àuthenticate`, y la función `gettext_lazy` en caso de tener archivo de traducción. Serializamos los campos que necesitamos, y en caso de la contraseña la estilizamos. Luego, creamos una función para validar y autenticar el usuario el cuál se retorna, en coso de error se arroja un mensaje.

```py
from django.contrib.auth import ..., authenticate
from django.utils.translation import gettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style = {
            'input_type': 'password'
        },
        trim_whitespace = False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
```

## Vistas

Procedemos a crear la vista para nuestra api del token.

```py
...
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import ..., AuthTokenSerializer

...
class CreateTokenView(ObtainAuthToken):
    """ Obtener nuevo auth token para el usuario """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
```

Registramos nuestra vista en el archivo `user/urls.py`:

```py
urlpatterns = [
    ...,
    path('token/', views.CreateTokenView.as_view(), name='token')
]
```

Corremos el proyecto para visualizarlo en el navegador, para ello usamos el comando:

```txt
python manage.py runserver
```

Ingresamos al endpoint `http://127.0.0.1:8000/api/user/` y nos muestras las rutas a las que podemos ir dentro de dicho módulo.

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [API Crear Usuarios](11_API_Crear_Usuarios.md) | [Readme](../../README.md) | [User Endpoint](13_User_Endpoint.md) |
