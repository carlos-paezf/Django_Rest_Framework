# Etiquetas

Dentro del archivo `app/settings.py` registramos nuestra nueva aplicación:

```py
# Application definition

INSTALLED_APPS = [
    ...,
    'recipe'
]
```

## Modelo

Creamos el test del nuevo modelo dentro de `core/tests/test_model.py`:

```py
...
from core import models


def sample_user(email='test@test.com', password='test_123'):
    """ Crear usuario de ejemplo """
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    ..
    def test_tag_str(self):
        """ > Probar representación en cadena de texto del tag """
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Meat'
        )

        self.assertEqual(str(tag), tag.name)
```

Dentro del archivo `core/models.py` creamos el modelo para las etiquetas, el cual tiene una relación 1:1 con un usuario:

```py
class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
```

En el archivo `core/admin.py`, registramos el modelo:

```py
admin.site.register(models.Tag)
```

Como hemos hecho modificaciones el modelo, debemos hacer las migraciones:

```txt
python manage.py makemigrations
```

```txt
python manage.py migrate
```

## Listar Etiquetas

Creamos un nuevo archivo llamado `recipe/tests/test_tags_api.py`, y hacemos las importaciones necesarias:

```py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer
```

Creamos la url de los tags, y luego creamos 2 clases. La primera clase se encarga de probar las funciones publicas del API de tags, las cuales en este caso no tiene. La segunda clase testea la funcionalidad de la API privada; necesitamos que se listen las etiquetas ordenadas por nombre, y que los resultados se limiten a las etiquetas del usuario:

```py
...
TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """ > Probar API de tags sin autenticación """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ > Probar que se requiere iniciar sesión para obtener tags """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ > Probar API de tags con autenticación """

    def setUp(self):
        self.user = get_user_model().objects.create_user('test@test.com', 'test_123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ > Probar que se pueden obtener tags """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ > Probar que se limitan los tags a un usuario """
        user2 = get_user_model().objects.create_user('user2@test.com', 'test_123')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
```

Creamos el archivo para los serializadores dentro de la app de `recipe`:

```py
from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serializador para objeto tag """
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
```

Dentro del archivo `recipe/views.py`, creamos el ViewSet para los tags:

```py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Manejar Tags en la base de datos """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """ Obtener tags del usuario actual """
        return self.queryset.filter(user=self.request.user).order_by('-name')
```

Creamos el archivo `recipe/urls.py`, y registramos nuestra vista como una ruta:

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
```

En el archivo `app/urls.py`, registramos el conjunto de urls para las recetas:

```py
urlpatterns = [
    ...,
    path('api/recipe/', include('recipe.urls')),
]
```

Añadimos 2 tests más para cuando se crea un tag de manera correcta y/o incorrecta:

```py
class PublicTagsApiTests(TestCase):
    ...
    def test_create_tag_successful(self):
        """ > Probar que se puede crear un tag """
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ > Probar que no se puede crear un tag con datos inválidos """
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

Implementamos la lógica en nuestra vista:

```py

```

| Anterior                              |                           | Siguiente                          |
| ------------------------------------- | ------------------------- | ---------------------------------- |
| [App para Recetas](14_App_Recetas.md) | [Readme](../../README.md) | [Ingredientes](16_Ingredientes.md) |
