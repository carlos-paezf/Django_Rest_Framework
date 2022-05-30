# Crear un ViewSet

Para crear un ViewSet, necesitamos hacer la importación del módulo `viewsets` desde `rest_framework`:

```py
from rest_framework import viewsets
```

Luego, creamos una clase que va a heredar de la clase `ViewSet` del módulo que acabamos de importar. El primer método que vamos a usar, es la función `list()`:

```py
class HelloWorldViewSet(viewsets.ViewSet):
    
    def list(self, request):
        a_viewset = [
            'Usa acciones como list, create, retrieve, update, partial_update, delete'
            'Automáticamente mapea a los URLs usando Routers',
            'Provee más funcionalidad con menos código'
        ]

        return Response({
            'message': 'Hola',
            'a_viewset': a_viewset
        })
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [¿Qué son los ViewSets?](14_Que_es_ViewSet.md) | [Readme](../README.md) | [Agregar URL Router](16_Agregar_URL_Router.md) |
