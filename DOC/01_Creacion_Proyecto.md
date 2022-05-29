# Creación del proyecto

Creamos un nuevo proyecto de Django con el siguiente comando:

```txt
django-admin startproject profiles_project .
```

## Creación de la app `profiles_api`

Vamos a observar que se nos crea un directorio llamado `profiles_project`. Necesitamos crear una app dentro de dicha carpeta, la cual nos va a permitir darle funcionalidad a nuestro sitio, para lo cual empleamos el siguiente comando:

```txt
python manage.py startapp profiles_api
```

## Configurando `settings.py`

Necesitamos registrar nuestra app `profiles_api` dentro la configuración de nuestro proyecto, junto al paquete de `rest_framework`, por lo que dentro del archivo `profiles_project/settings.py`, en la sección de `INSTALLED_APPS` añadimos nuevos elementos:

```py
# Application definition

INSTALLED_APPS = [
    ...,

    'rest_framework',
    'rest_framework.authtoken',
    
    'profiles_api',
]
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
|          | [Readme](../README.md) | [Modelo de Usuarios](02_Modelo_Usuarios.md) |
