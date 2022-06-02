# Test para Modelo de Usuario Personalizado

Como se mencionaba en la sección anterior, vamos a estar trabajando basados en tests (***TDD***), por lo tanto primero desarrollamos los test y luego creamos los modelos. Lo primero será instalar el app `core` dentro de nuestro proyecto, por lo tanto vamos al archivo `app/settings.py` y hacemos la siguiente modificación:

```py
# Application definition

INSTALLED_APPS = [
    ...,
    'core',
]
```

Creamos el archivo `core/tests/test_models.py`, en el que tendremos una clase para hacer las pruebas con nuestro modelos. Dicha clase va a heredar de `TestCase` de `django.test`. La primera prueba consiste en crear de manera correcta un usuario con un correo, para ello creamos el email y la contraseña, y luego usamos la función `get_user_model()` para traer todos sus objetos y ejecutar el método `create_user()`. La prueba pasará si el correo coincide con el correo del modelo, y si la contraseña logra ser verificada.

```py
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
```

Para ejecutar nuestras pruebas, usamos el comando:

```py
python manage.py test
```

La prueba va a fallar ya que por defecto para crear un usuario se require de un `username`, lo que haremos en la próxima sección será modificar el modelo de usuario para poder crear o ingresar con el correo.

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
|[Creando App Core](02_Creando_App_Core.md) | [Readme](../../README.md) | [Modelo de Usuario Personalizado](04_Modelo_Usuario_Personalizado.md) |
