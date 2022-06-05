# API Crear Usuarios

## Test

Vamos a crear un archivo llamado `user/tests/test_user_api.py`, en donde tendremos nuestro test unitarios. Lo primero será crear una constante para la url a la que estaremos accediendo, junto a una función para crear un usuario a partir de ciertos parámetros.

```py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')

def createUser(**params):
    return get_user_model().objects.create_user(**params)
```

Luego, creamos una clase para ejecutar las pruebas que se pueden realizar dentro de nuestra api pública, tales como crear un usuario de manera correcta, validar que un usuario ya existe, o verificar que la contraseña es muy corta.

```py
class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test name'
        }
        createUser(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@test.com',
            'password': '123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
```

## API

Vamos a crear un serializador, por lo que añadimos el archivo `user/serializers.py` y dentro tendremos la clase `UserSerializer`, con la configuración de los campos que necesitamos:

```py
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
```

Vamos a crear un archivo llamado `user/urls.py`, en el que registraremos las urls de nuestras vistas:

```py
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
```

Registramos las urls locales dentro del archivo `app/urls.py`:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', include('user.urls')),
]
```

Dentro del archivo `user/views.py` vamos a crear las vistas necesarias:

```py
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Crear nuestro usuario en el sistema """
    serializer_class = UserSerializer
```

Ya teniendo esto, corremos los tests y podremos observar que todos pasan.

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Crear App de Usuarios](10_Crear_App_Usuarios.md) | [Readme](../../README.md) | [Token API](12_Token_API.md) |
