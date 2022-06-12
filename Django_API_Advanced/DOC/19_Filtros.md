# Filtros

Vamos a darle la funcionalidad a nuestra aplicación, de poder hacer diversos filtros, para ello vamos a `recipe/tests/test_recipes_api.py` y creamos primero los test para filtrar recetas por tags o por ingredientes:

```py
class RecipeImageUploadTests(TestCase):
    ...
    def test_filter_recipes_by_tags(self):
        """ > Probar que se pueden filtrar recetas por tags """
        recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
        recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
        tag1 = sample_tag(user=self.user)
        tag2 = sample_tag(user=self.user)
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')

        res = self.client.get(
            RECIPE_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
        
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
    
    def test_filter_recipes_by_ingredients(self):
        """ > Probar que se pueden filtrar recetas por ingredientes """
        recipe1 = sample_recipe(user=self.user, title='Pancakes')
        recipe2 = sample_recipe(user=self.user, title='Porridge')
        ingredient1 = sample_ingredient(user=self.user)
        ingredient2 = sample_ingredient(user=self.user)
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')

        res = self.client.get(
            RECIPE_URL,
            {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
        )

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
```

Ahora vamos a `recipe/views.py` y añadimos lo siguiente:

```py
class RecipeViewSet(viewsets.ModelViewSet):
    ...
    def _params_to_ints(self, query_params):
        """ Convertir los parámetros a enteros """
        return [int(str_id) for str_id in query_params.split(',')]

    def get_queryset(self):
        """ Obtener recetas del usuario actual """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')

        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        
        return queryset.filter(user=self.request.user)
```

Ahora vamos a `recipe/tests/test_tags_api.py` y creamos los tests para filtrar los tags basados en receta:

```py
from core.models import ..., Recipe
...
class PrivateTagsApiTests(TestCase):
    ...
    def test_retrieve_tags_assigned_to_recipes(self):
        """ > Probar que se pueden obtener tags asignados a recetas """
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Coriander eggs on toast',
            time_minutes=10,
            price=5.00,
            user=self.user
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
    
    def test_retrieve_tags_assigned_unique(self):
        """ > Probar que se pueden obtener tags asignados a recetas """
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=3.00,
            user=self.user
        )
        recipe1.tags.add(tag)
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=2.00,
            user=self.user
        )
        recipe2.tags.add(tag)
        
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
```

Ahora vamos a ir al archivo `recipe/views.py` y añadimos lo siguiente:

```py
class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    ...
    def get_queryset(self):
        """ Obtener tags del usuario actual """
        assigned_only = bool(self.request.query_params.get('assigned_only', 0))

        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()
```

| Anterior                                                          |                           | Siguiente |
| ----------------------------------------------------------------- | ------------------------- | --------- |
| [Configurar imágenes en Django](18_Configurar_Imagenes_Django.md) | [Readme](../../README.md) |           |
