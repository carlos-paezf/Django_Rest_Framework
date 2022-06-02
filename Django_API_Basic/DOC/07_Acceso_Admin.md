# Acceso Admin

Debemos definir a que modelos tiene acceso nuestro Admin, en estos momentos queremos que tenga acceso al modelo de usuarios, por lo que nos dirigimos al archivo `profiles_api/admin.py` e importamos nuestro archivo de modelos. Luego registramos el modelo de usuarios:

```py
from django.contrib import admin

from profiles_api import models


admin.site.register(models.UserProfile)
```

Para probar que si tenemos el acceso como admin al modelo de usuarios, levantamos el servidor con el siguiente comando:

```txt
python manage.py runserver
```

E ingresamos a la ruta que se nos muestra para el desarrollo (Al momento actual es `http://127.0.0.1:8000/`). Para ir a la página de administración, añadimos el endpoint `/admin`, lo cual nos muestra un formulario de ingreso en el que ponemos las credenciales que habíamos determinado antes. Si registramos bien el modelo, dentro de la sección `PROFILES_API` podemos observar un elemento llamado `User profiles`, en el que tenemos la opción de editar o registrar nuestros usuarios.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Super-Usuario](06_Super_Usuario.md) | [Readme](../README.md) | [¿Que es una APIView?](08_Que_es_APIView.md) |
