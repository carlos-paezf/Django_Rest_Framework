# Configurar Imágenes en Django

Para manejar imágenes, debemos instalar un paquete llamado `pillow`, podemos consultar la versión en [pypi.org](pypi.org). Dentro de nuestro archivo `requirements.txt` añadimos la siguiente línea:

```txt
...
pillow==9.1.1
```

Luego usamos el siguiente comando para instalar el paquete:

```txt
pip install -r requirements.txt
```

Ahora, vamos al archivo `app/settings.py` e indicamos la url de los recursos de media:

```py
STATIC_URL = 'static/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/static_root/'
MEDIA_ROOT = '/media_root/'
```

Dentro de `app/urls.py` importamos lo siguiente;

```py
...
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    ...,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Modelo para ingresar imágenes a la API

Vamos a crear el test para el próximo modelo, por lo que vamos a `core/tests/test_models.py` y añadimos lo siguiente:

```py
...
from unittest.mock import patch
...
class ModelTest(TestCase):
    ...
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ > Probar que el nombre del archivo de la receta es un UUID """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipes/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
```

Ahora, vamos a `core/models.py` y creamos el modelo respectivo:

```py
...
import uuid
import os

def recipe_image_file_path(instance, filename):
    """ Generar el file path para la imagen de la receta """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipes/', filename)

...

class Recipe(models.Model):
    """ Modelo de la Receta """
    ...
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    ...
```

Como hemos hecho modificaciones el modelo, debemos hacer las migraciones:

```txt
python manage.py makemigrations
```

```txt
python manage.py migrate
```

## Subir imágenes

Vamos al archivo `recipe/tests/test_recipe_api.py` y hacemos la siguiente modificación:

```py
import tempfile
import os
from PIL import Image
...
def image_upload_url(recipe_id):
    """ Devuelve la URL para subir una imagen de una receta """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])

...

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
```

Proseguimos con la serialización de las imágenes, por lo que vamos a `recipe/serializers.py`:

```py
class RecipeImageSerializer(serializers.ModelSerializer):
    """ Serializador para objeto recipe con imagen """

    class Meta:
        model = Recipe
        fields = ('id', 'image',)
        read_only_fields = ('id',)
```

Vamos a `recipe/views.py` y configuramos la vista:

```py
...
from rest_framework import ..., status
from rest_framework.response import Response
from rest_framework.decorators import action
...
class RecipeViewSet(viewsets.ModelViewSet):
    ...
    def get_serializer_class(self):
        """ Obtener el serializador dependiendo del método """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class
    ...
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Subir una imagen a la receta """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

| Anterior                 |                           | Siguiente                |
| ------------------------ | ------------------------- | ------------------------ |
| [Recetas](17_Recetas.md) | [Readme](../../README.md) | [Filtros](19_Filtros.md) |
