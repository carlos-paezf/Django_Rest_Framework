from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def createUser(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """ > Probar el API pública del usuario """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ > Probar crear usuario con el payload exitoso """
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
        """ > Probar crear un usuario que ya existe: falla """
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test name'
        }
        createUser(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ > Probar que la contraseña sea mayor a 5 caracteres """
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

    def test_create_token_for_user(self):
        """ > Probar que el token será creado para el usuario """
        payload = {
            'email': 'test@test.com',
            'password': 'test_123',
            'name': 'Test name'
        }
        createUser(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ > Probar que el token no es creado con credenciales invalidas """
        createUser(email='test@test.com', password='testpass')
        payload = {
            'email': 'test@test.com',
            'password': 'testwrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ > Probar que no se creó el token si no existe el usuario """
        payload = {
            'email': 'test@test.com',
            'password': 'testwrong',
            'name': 'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ > Probar que el email y la contraseña sean requeridas """
        res = self.client.post(TOKEN_URL, { 'email': 'one', 'password': '' })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
