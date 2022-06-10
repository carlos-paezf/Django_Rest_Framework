# Ingredientes

## Modelo

Dentro del archivo `core/tests/test_model.py`, añadimos un nuevo test para cuando se añade un ingrediente:

```py
class ModelTest(TestCase):
    ...
    def test_ingredient_str(self):
        """ > Probar representación en cadena de texto del ingrediente """
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
```

El archivo `core/model.py`, creamos el modelo de los ingredientes:

```py
class Ingredient(models.Model):
    """ Modelo del Ingrediente para la receta """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
```

Luego añadimos el nuevo modelo a la zona de administración, mediante el registro en el archivo `core/admin.py`:

```py
admin.site.register(models.Ingredient)
```

Como hemos hecho modificaciones el modelo, debemos hacer las migraciones:

```txt
python manage.py makemigrations
```

```txt
python manage.py migrate
```

## Listar ingredientes

Creamos un nuevo archivo llamado `recipe/tests/test_ingredients_api.py`, en el cual haremos los test para los ingredientes, ya sea desde la parte pública o la zona privada. Las pruebas son similares a las realizadas con los tags:

```py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """ > Probar el API de acceso público de los ingredientes """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ > Probar que se requiere iniciar sesión para acceder al API """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ > Probar el API de acceso privado de los ingredientes """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@test.com', 'testpass')

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ > Probar que se puede obtener una lista de ingredientes """
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ > Probar que se limitan los ingredientes a un usuario """
        user2 = get_user_model().objects.create_user('test2@test.com', 'testpass')
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """ > Probar que se puede crear un ingrediente """
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ > Probar que no se puede crear un ingrediente con datos inválidos """
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

Luego creamos la vista dentro de `recipe/views.py`:

```py
...
from core.models import ..., Ingredient
...
class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """ Manejar Ingredientes en la base de datos """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """ Obtener ingredientes del usuario actual """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Crear nuevo ingrediente """
        serializer.save(user=self.request.user)
```

Registramos la vista como ruta en `recipe/urls.py`:

```py
...
router.register('ingredients', views.IngredientViewSet)
...
```

## Optimización de Código

Vamos a simplificar el archivo `recipes/views.py` creando una clase base, para luego heredar:

```py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """ Base viewset para obtener y crear objetos de un modelo """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Obtener tags del usuario actual """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Crear nuevo tag """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manejar Tags en la base de datos """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manejar Ingredientes en la base de datos """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
```

| Anterior                     |                           | Siguiente                |
| ---------------------------- | ------------------------- | ------------------------ |
| [Etiquetas](15_Etiquetas.md) | [Readme](../../README.md) | [Recetas](17_Recetas.md) |
