# Migraciones de Base de Datos

El archivo de migraciones es empleado para poder configurar la base de datos, de acuerdo a los modelos de nuestro proyecto en Django. Las migraciones las hacemos cada que cambiamos el archivo de modelos, esto con el fin de hacer un match entre la DB y la nueva configuración de los modelos. Las migraciones son el método más seguro para hacer cambios a la base de datos una vez que el proyecto se encuentre en producción, puesto que nos evita errores tales como datos vacíos en los registros anteriores al cambio.

Para crear las migraciones de una app especifica (en nuestro caso `profiles_api`), usamos el siguiente comando:

```txt
python manage.py makemigrations profiles_api
```

Para ejecutar las migraciones usamos el siguiente comando:

```txt
python manage.py migrate
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Modelo de Usuario Personalizado](04_Modelo_Usuario_Personalizado.md) | [Readme](../../README.md) | [Super-Usuario](06_Super_Usuario.md) |
