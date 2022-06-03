from django.test import TestCase
from django.contrib.auth import get_user_model


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
