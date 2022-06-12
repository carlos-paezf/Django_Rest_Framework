from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
import tempfile
import os
from PIL import Image


RECIPE_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    """ Devuelve la URL para subir una imagen de una receta """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])

def sample_tag(user):
    """ Crear un tag de ejemplo """
    return Tag.objects.create(user=user, name='mexican')

def sample_ingredient(user):
    """ Crear un ingrediente de ejemplo """
    return Ingredient.objects.create(user=user, name='Cucumber')

def detail_url(recipe_id):
    """ Devuelve la URL de detalle de una receta """
    return reverse('recipe:recipe-detail', args=[recipe_id])

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
        
    def test_view_recipe_detail(self):
        """ > Probar que se puede ver una receta """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

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


class RecipeImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user@test.com', 'testpass')
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """ > Probar que se puede subir una imagen a una receta """
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))
    
    def test_upload_image_bad_request(self):
        """ > Probar que no se puede subir una imagen a una receta """
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
