# Super-Usuario

El SuperUsuario nos permite tener una vista dentro de la página web, para poder acceder mediante ella a nuestros modelos como administradores. Para crear un super-usuario usamos el siguiente comando:

```txt
python manage.py createsuperuser
```

Se nos va a pedir algunos datos: Email (cpaezferreira@gmail.com), Name (David Ferrer), Password (admin_1234567890). Si todo está bien, nos aparece el mensaje `Superuser created successfully`. La manera en que se pidieron los datos, fue establecida por nosotros dentro de la función `create_superuser()` en la clase `UserProfileManager`.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Migraciones de Base de Datos](05_Migraciones_Base_Datos.md) | [Readme](../../README.md) | [Acceso de Admin](07_Acceso_Admin.md) |
