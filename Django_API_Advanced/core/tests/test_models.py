from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='test@test.com', password='test_123'):
    """ Crear usuario de ejemplo """
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):
    def test_create_user_with_email_succesful(self):
        """ > Probar la creación de un nuevo usuario con un email, de manera correcta """
        email = 'test@gmail.com'
        password = 'test_123'
        user = get_user_model().objects.create_user(email = email, password = password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ > Probar que el correo de un nuevo usuario está normalizado """
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, '123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ > Probar error de creación de usuario con email invalido """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_super_user(self):
        """ > Probar super-usuario creado """
        user = get_user_model().objects.create_superuser('admin@gmail.com', 'admin_1234567890')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ > Probar representación en cadena de texto del tag """
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Meat'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ > Probar representación en cadena de texto del ingrediente """
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ > Probar representación en cadena de texto de la receta """
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mushroom sauce',
            time_minutes = 5,
            price = 5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ > Probar que el nombre del archivo de la receta es un UUID """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipes/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
