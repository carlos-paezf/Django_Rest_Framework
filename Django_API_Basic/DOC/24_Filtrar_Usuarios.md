# Filtrar usuarios

Vamos a agregar algunos filtros para traer la información según algunos campos. Importamos el módulo `filters` de `rest_framework`, y luego añadimos las tuplas dentro de la clase para saber con cual tipo de filtro vamos a trabajar, y sobre cuales campos:

```py
from rest_framework import filters


class UserProfileViewSet(viewsets.ModelViewSet):
    ...
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email')
```

Para probar los filtros vamos al endpoint `http://localhost:8000/api/profile/` y tendremos la opción `Filters`. Lo que hace básicamente es añadir una query a la url con la información que pongamos en el input del filtro.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Autenticación y Permisos de ViewSet](23_Autenticacion_Permisos_ViewSet.md) | [Readme](../README.md) | [Área de Login](25_Area_Login.md) |
