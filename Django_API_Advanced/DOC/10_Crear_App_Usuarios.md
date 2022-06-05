# Crear App de Usuarios

Vamos a crear una nueva app para el CRUD de los usuarios, ello lo hacemos con el comando:

```txt
python manage.py startapp user
```

Las migraciones las vamos a mantener dentro del app `core`, por lo tanto borramos el directorio de `migrations`, hacemos lo mismo para los archivos `admin.py`, `models.py` y `test.py`. Para el caso del último, creamos un nuevo directorio llamado `user/tests`, en el que involucraremos los tests necesarios (importante crear el archivo `__init__.py` dentro de dicho directorio).

Registramos nuestra app `user` en el archivo `app/settings.py`, pero también debemos instanciar los paquetes `rest_framework` y `rest_framework.authtoken`:

```py
# Application definition

INSTALLED_APPS = [
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...
    'user',
]
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
|  [Agregar Usuario desde Admin](09_Agregar_Usuario_Desde_Admin.md) | [Readme](../../README.md) | [API Crear Usuarios](11_API_Crear_Usuarios.md) |
