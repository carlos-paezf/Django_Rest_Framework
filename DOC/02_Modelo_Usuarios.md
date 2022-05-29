# Modelo de Usuarios

Django ya ofrece un modelo propio para los usuarios, pero nosotros la vamos a editar para nuestra conveniencia. Lo primero será ir al archivo `profiles_api/models.py` y hacer la importación del modelo `AbstractBaseUser`, junto a la clase `PermissionsMixin` para añadir los campos y métodos necesarios que soportan los modelos `Group` y `Permission` usando el `ModelBackend`:

```py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
```

## Definición del Modelo

Una vez hechas las importaciones, creamos nuestra clase `UserProfile` que heredará de las dos clases que acabamos de importar, y dentro de la cuál definimos el modelo de la base de datos para los usuarios de nuestro sistema:

```py
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
```

## ModelManager

Ahora, necesitamos establecer el ModelManager que es requerido para usar nuestro modelo personalizado con Django CLI:

```py
class UserProfile(AbstractBaseUser, PermissionsMixin):
    ...
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
```

## Métodos

Creamos un método para obtener el nombre completo, y el nombre corto de usuario, junto al método que contiene la cadena representativa del usuario

```py
class UserProfile(AbstractBaseUser, PermissionsMixin):
    ...
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Creación del proyecto](01_Creacion_Proyecto.md) | [Readme](../README.md) | [Agregando Manager de Usuario](03_Agregando_Manager_Usuario.md) |
