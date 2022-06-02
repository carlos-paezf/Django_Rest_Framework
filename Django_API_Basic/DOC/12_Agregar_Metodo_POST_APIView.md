# Agregar método POST al APIView

Dentro del archivo `profiles_api/views.py`, importamos el módulo `status` de `rest_framework`, y nuestros serializers. `status` nos brinda diversos códigos de respuesta para nuestra api.

```py
from rest_framework import status
from profiles_api import serializers
```

Dentro de nuestra clase `HelloWorldAPIView`, creamos una instancia de nuestra clase `HelloWorldSerializers` para tener acceso a sus métodos, los cuales han sido heredados de `Serializer`.

```py
class HelloWorldAPIView(APIView):
    serializer_class = serializers.HelloWorldSerializers
```

El método `post()` definimos una variable que serializa la data que se está recibiendo del request, y luego la validamos. En caso de ser valida, extraemos el campo `name` y lo ponemos en un string que será enviado mediante la Response. En caso de que el serializer no sea valido, retornamos los errores y enviamos un código de estado 400:

```py
class HelloWorldAPIView(APIView):
    ...
    def post(self, request):
        """ Crear un mensaje con nuestro nombre """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'message': message
            })
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
```

Para probar nuestra función `post()`, ingresamos al endpoint `http://127.0.0.1:8000/api/hello-view`, y podremos observar que en la parte inferior tenemos un formulario para el campo `name`, el cual tiene la validación de no pasar los 10 caracteres. Una vez enviada la data, recibimos nuestro mensaje en la response.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Crear Serializador](11_Crear_Serializador.md) | [Readme](../../README.md) | [Métodos PUT, Patch y Delete](13_Metodos_PUT_PATCH_DELETE.md) |
