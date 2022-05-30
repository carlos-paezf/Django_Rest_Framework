# Crear Serializador

Un serializador nos permite convertir objetos de Python en JSON y viceversa. Es similar a un formulario de Django, en el que se definen los campos que se quieren convertir en JSON. Entonces, si tenemos planeado recibir información mediante el método POST, es indispensable tener el serializador.

Vamos a crear un archivo llamado `serializers.py` dentro de la app `profiles_api`. Es buena práctica tener todos los serializadores dentro de dicho archivo, para no tener problemas al momento de la búsqueda de los mismos. Lo primero será importar el módulo `serializers` de `rest_frameworks`, para luego hacer que nuestra clase herede de la clase `Serializer`, y serializar el campo `name`:

```py
from rest_framework import serializers


class HelloWorldSerializers(serializers.Serializer):
    name = serializers.CharField(max_length = 10)
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [URL de APIView](10_URL_APIView.md) | [Readme](../README.md) | [Agregar método POST al APIView](12_Agregar_Metodo_POST_APIView.md) |
