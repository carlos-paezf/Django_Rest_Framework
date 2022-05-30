# Métodos PUT, Patch y Delete

Vamos a crear el enunciado de los métodos `put()`, `patch()` y `delete()`, puesto que aún no tenemos una base de datos con elementos sobre los que podamos aplicar los métodos:

```py
class HelloWorldAPIView(APIView):
    ...
    def put(self, request, pk=None):
        """ Actualizar un objeto """
        return Response({ 'method': 'PUT' })

    def patch(self, request, pk=None):
        """ Actualizar parcialmente un objeto """
        return Response({ 'method': 'PATCH' })

    def delete(self, request, pk=None):
        """ Eliminar un objeto """
        return Response({ 'method': 'DELETE' })
```

De nuevo, podemos hacer la prueba de los métodos con la url `http://127.0.0.1:8000/api/hello-view`. Para usar los métodos de PUT y PATCH, alternamos entre las opciones de `Raw Data` y `HTML Form` que aparecen en la parte final de la interfaz.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Agregar método POST al APIView](12_Agregar_Metodo_POST_APIView.md) | [Readme](../README.md) | [¿Qué son los ViewSets?](14_Que_es_ViewSet.md) |
