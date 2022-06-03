# Normalización de Correos

## Test de normalización

Teniendo en cuenta el TDD, vamos a crear primero el test respectivo, por lo tanto vamos a `core/tests/test_models.py` y creamos la siguiente prueba:

```py
class ModelTest(TestCase):
    ...
    def test_new_user_email_normalized(self):
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, '123')

        self.assertEqual(user.email, email.lower())
```

Para ejecutar los test usamos el siguiente comando:

```txt
python manage.py test
```

## Corrección del Modelo

Para normalizar nuestro email, vamos al modelo `UserManager` y aplicamos el siguiente cambio:

```py
class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        user = self.model(email = self.normalize_email(email), **extra_fields)
        ...
```

### Validación del email

Creamos un test para verificar que se arroje un error en caso de que se intente enviar vacío el campo de email. Como aún no está configurado el modelo para dicha validación, nuestro test no va a pasar.

```py
class ModelTest(TestCase):
    def test_new_user_invalid_email(self):
        """ > Probar error de creación de usuario con email invalido """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')
```

Implementamos la lógica dentro del modelo:

```py
class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')
        ...
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Modelo de Usuario Personalizado](04_Modelo_Usuario_Personalizado.md) | [Readme](../../README.md) | [Crear SuperUsuario](06_Crear_SuperUser.md) |
