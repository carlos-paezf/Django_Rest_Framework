# Creando RetrieveUpdate, PartialUpdate y Destroy

Creamos las funciones para crear, obtener un elemento por su id, actualización total y parcial, y eliminación de un objeto. Al igual que en las APIViews, necesitamos un serializador, por lo tanto usamos el mismo que tenemos para la otra clase:

```py
class HelloWorldViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloWorldSerializers

    ...
    def create(self, request):
        """ Crear un nuevo mensaje """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola mundo {name}'s
            return Response({ 'message': message })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Obtener un objeto y su id """
        return Response({ 'http_method': 'GET' })

    def update(self, request, pk=None):
        """ Actualizar un objeto """
        return Response({ 'http_method': 'PUT' })

    def partial_update(self, request, pk=None):
        """ Actualizar parcialmente un objeto """
        return Response({ 'http_method': 'PATCH' })

    def destroy(self, request, pk=None):
        """ Eliminar un objeto """
        return Response({ 'http_method': 'DELETE' })
```

Para probar los métodos, vamos al endpoint `http://127.0.0.1:8000/api` e ingresamos a la ruta que se muestra en el objeto JSON. Cuando tenemos la ruta general, estamos en el método GET y tenemos la opción de POST, pero cuando pasamos un id dentro de la URL, podemos tener los métodos de PUT, PATCH y DELETE.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Agregar URL Router](16_Agregar_URL_Router.md) | [Readme](../../README.md) | [API para perfil de usuario](18_API_Perfil_Usuario.md) |
