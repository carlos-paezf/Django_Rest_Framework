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
