# Agregando Manager de Usuario

Dado que creamos un modelo personalizado de usuarios, necesitamos especificarle a Django como vamos a procesar nuestros usuarios, por lo tanto seguimos creando funcionalidades dentro del archivo `profiles_api/models.py`.

## Manejador de perfiles de usuario

Necesitamos importar la clase `BaseUserManager`, la cuál será la clase padre de nuestra nueva clase `UserProfileManager`. Luego, dentro de la nueva clase, definimos los métodos para la manipulación de los usuarios.

```py
from django.contrib.auth.models import BaseUserManager
```

### Crear un usuario

Para crear un usuario necesitamos su email y su nombre, por el momento no solicitamos su contraseña. Se valida que el usuario tenga un email y luego se normaliza pasando el dominio a minúsculas. Se crear el usuario con el email y el nombre, se determina la contraseña, y por último se guarda y retornar el usuario.

```py
class UserProfileManager(BaseUserManager):
    
    def create_user(self, email, name, password = None):
        if not email:
            raise ValueError('Usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email = email, name = name)

        user.set_password(password)
        user.save(using = self._db)

        return user
```

### Crear un super-usuario

También tenemos una función para crear un super-usuario, el cuál si requiere de una contraseña, además de que al heredar de la clase `PermissionMixin` podemos configurar la propiedad `is_superuser`

```py
class UserProfileManager(BaseUserManager):
    ...
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Modelo de Usuarios](02_Modelo_Usuarios.md) | [Readme](../README.md) | [Modelo de Usuario Personalizado](04_Modelo_Usuario_Personalizado.md) |
