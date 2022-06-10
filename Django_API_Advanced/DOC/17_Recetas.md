# Recetas

## Modelo

Para nuestras recetas, vamos a crear una nuevo test dentro de `core/tests/test_models.py`:

```py
class ModelTest(TestCase):
    ...
    def test_recipe_str(self):
        """ > Probar representación en cadena de texto de la receta """
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mushroom sauce',
            time_minutes = 5,
            price = 5.00
        )

        self.assertEqual(str(recipe), recipe.title)
```

Creamos el modelo en `core/models.py`, pero este modelo tendrá la cualidad de tiene una relación n:n con los ingredientes, al igual que los tags:

```py
class Recipe(models.Model):
    """ Modelo de la Receta """
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
```

Registramos nuestro modelo dentro de `core/admin.py`:

```py
...
admin.site.register(models.Recipe)
```

Como hemos hecho modificaciones el modelo, debemos hacer las migraciones:

```txt
python manage.py makemigrations
```

```txt
python manage.py migrate
```

## Listar las recetas

Creamos un archivo llamado `recipe/tests/test_recipes_api.py` y ponemos nuestras pruebas:

```py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """ Crear una receta de ejemplo """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Pruebas de la API de recetas públicas """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ > Probar que se requiere iniciar sesión para acceder a la API """
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
class PrivateRecipeApiTests(TestCase):
    """ Pruebas de la API de recetas privadas """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@test.com', 'test_123')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """ > Probar que se pueden obtener recetas """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """ > Probar que las recetas solo se pueden obtener del usuario """
        user2 = get_user_model().objects.create_user('test2@test.com', 'test_123')
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
```

Siguiente, creamos el serializador del modelo dentro de `recipe/serializers.py`, teniendo en mente las relaciones con los otros modelos:

```py
...
from core.models import ..., Recipe
...
class RecipeSerializer(serializers.ModelSerializer):
    """ Serializador para objeto recipe """

    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'price', 'time_minutes', 'link',)
        read_only_fields = ('id',)
```

Vamos al archivo `recipe/views.py` y creamos la vista de nuestro modelo:

```py
class RecipeViewSet(viewsets.ModelViewSet):
    """ Manejar las recetas en la base de datos """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Obtener recetas del usuario actual """
        return self.queryset.filter(user=self.request.user)
```

Registramos la vista dentro de `recipe/urls.py`:

```py
...
router.register('recipes', views.RecipeViewSet)
```

## Obtener detalles específicos de la receta

Queremos tener la información detallada de una receta, entonces definimos el test respectivo para esta tarea dentro de `recipe/tests/test_recipes_api.py`:

```py
def sample_tag(user):
    """ Crear un tag de ejemplo """
    return Tag.objects.create(user=user, name='mexican')

def sample_ingredient(user):
    """ Crear un ingrediente de ejemplo """
    return Ingredient.objects.create(user=user, name='Cucumber')

def detail_url(recipe_id):
    """ Devuelve la URL de detalle de una receta """
    return reverse('recipe:recipe-detail', args=[recipe_id])

...

class PrivateRecipeApiTests(TestCase):
    ...
     def test_view_recipe_detail(self):
        """ > Probar que se puede ver una receta """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
```

Definimos el serializador para los detalles de la receta, dentro de `recipe/serializers.py`:

```py
...
class RecipeDetailSerializer(RecipeSerializer):
    """ Serializador para objeto recipe con detalles """
    ingredients = IngredientSerializer(many = True, read_only = True)
    tags = TagSerializer(many = True, read_only = True)
```

También creamos una método para la vista `RecipeViewSet` dentro de `recipe/views.py`, con el fin de obtener el serializador dependiendo del método:

```py
class RecipeViewSet(viewsets.ModelViewSet):
    ...
    def get_serializer_class(self):
        """ Obtener el serializador dependiendo del método """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        
        return self.serializer_class
```

## Crear recetas

Volvemos al archivo de pruebas `recipe/tests/test_recipe_api.py` y añadimos:

```py
class PrivateRecipeApiTests(TestCase):
    ...
    def test_create_basic_recipe(self):
        """ > Probar que se puede crear una receta """
        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """ > Probar que se pueden crear recetas con tags """
        tag1 = sample_tag(user=self.user)
        tag2 = sample_tag(user=self.user)
        payload = {
            'title': 'Chocolate cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """ > Probar que se pueden crear recetas con ingredientes """
        ingredient1 = sample_ingredient(user=self.user)
        ingredient2 = sample_ingredient(user=self.user)
        payload = {
            'title': 'Chocolate cheesecake',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
```

Dentro de la clase `RecipeViewSet` del archivo `recipe/views.py`, añadimos la siguiente función:

```py
class RecipeViewSet(viewsets.ModelViewSet):
    ...
    def perform_create(self, serializer):
        """ Crear nueva receta """
        serializer.save(user=self.request.user)
```

| Anterior                     |                           | Siguiente                |
| ---------------------------- | ------------------------- | ------------------------ |
| [Ingredientes](16_Ingredientes.md) | [Readme](../../README.md) | [Configurar imágenes en Django](18_Configurar_Imagenes_Django.md) |
