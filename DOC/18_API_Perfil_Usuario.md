# API para perfil de usuario

## Que debemos hacer

1. Crear un nuevo perfil

   - Manejar el registro de nuevos usuarios
   - Validar datos del perfil

2. Listar perfiles existentes

   - Buscar perfiles
   - Email y nombre

3. Ver perfil especifico

   - ID del perfil

4. Actualizar perfil de usuarios logeados

   - Cambiar nombre, email y clave

5. Borrar perfil

## URLs de la API

- `/api/profile/`: Listar perfiles mediante HTTP GET, y crear un perfil mediante HTTP POST
- `/api/profile/<profile-id>/`: Ver perfil especifico mediante HTTP GET, actualizar la información mediante HTTP PUT, y borrar mediante HTTP DELETE.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Creando RetrieveUpdate, PartialUpdate y Destroy](17_Creando_RetrieveUpdate_PartialUpdate_Destroy.md) | [Readme](../README.md) | [Serializar perfil de usuario](19_Serializar_Perfil_Usuario.md) |
