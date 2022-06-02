# Agregando Ítem de modelo

Vamos a crear un nuevo modelo, por lo que dentro de `profiles_api/models.py` importamos el módulo `settings` de `django.conf` con el fin de obtener la configuración de nuestro proyecto, en este caso queremos obtener el valor de la variable `AUTH_USER_MODEL` que se encuentra dentro de `profiles_project/settings.py`:

```py
from django.conf import settings
```

Creamos una nueva clase para nuestro modelo, el cual contará con una llave foranea que apunta al modelo de Usuario:

```py
class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    status_text = models.CharField(max_length = 255)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.status_text
```

## Migrar el modelo

Debemos migrar nuestro modelo, por lo que usamos los siguientes comandos:

```txt
python manage.py makemigrations
```

```txt
python manage.py migrate
```

## Agregar el modelo al Admin de Django

Nos dirigimos al archivo `profile_api/admin.py` y registramos nuestro modelo:

```py
...
admin.site.register(models.ProfileFeedItem)
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [API para Feed de perfil de Usuario](26_API_Feed_Perfil_Usuario.md) | [Readme](../README.md) | [Serializador del Feed](28_Serializador_Feed.md) |
