# Modelo de Usuario Personalizado

Como ya establecimos el comportamiento de nuestro modelo de usuarios personalizados, ahora debemos hacer que sea reconocido por la aplicación en general como modelo de autenticación del usuario (registro e ingreso), para lo cual vamos al archivo `profiles_project/settings.py`, y agregamos un nuevo elemento al final del archivo:

```py
AUTH_USER_MODEL = 'profiles_api.UserProfile'
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Agregando Manager de Usuario](03_Agregando_Manager_Usuario.md) | [Readme](../README.md) | [Migraciones de Base de Datos](05_Migraciones_Base_Datos.md) |
