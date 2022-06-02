# Modelo de Usuario Personalizado

Vamos personalizar nuestro modelo, para ello vamos al archivo `core/models.py` e importamos algunas clases base:

```py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
```

Creamos nuestra clase `UserManager` que hereda de `BaseUserManager`, y modificamos el método de `create_user()`:

```py
class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
```

Creamos otro modelo que nos va a permitir la creación e ingreso del usuario mediante `email` en vez de `username`, además de que le definimos varios campos que vamos a utilizar.

```py
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
```

Luego vamos al archivo `app/settings.py` y en la parte final del mismo agregamos la configuración para que cualquier tema de autenticación, se realice en base al modelo que acabamos de crear:

```py
AUTH_USER_MODEL = 'core.User'
```

Como creamos un modelo, debemos hacer la migración del mismo, por lo tanto ejecutamos los siguientes comandos:

```txt
python manage.py makemigrations core
```

```txt
python manage.py migrate
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Test para Modelo de Usuario Personalizado](03_Test_Modelo_Usuario_Personalizado.md) | [Readme](../../README.md) | [Normalización de Correos](05_Normalizacion_Correos.md) |
