# Creando primer APIView

Vamos a crear nuestro primer APIView dentro del archivo `profiles_api/views.py`. Importamos de `rest_framework` las clases `APIView` y `Response`:

```py
from rest_framework.views import APIView
from rest_framework.response import Response
```

Creamos una clase que servirá de pruebas para nuestro primer APIView. Definimos el método `get()`, en el cual tenemos una lista que luego será retornada en formato JSON gracias a la clase `Response`, que en estos momentos está recibiendo un diccionario:

```py
class HelloWorldAPIView(APIView):
    
    def get(self, request, format=None):
        an_apiview = [
            'Usamos métodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional de Django',
            'Nos da el mayor control sobre la lógica de nuestra aplicación',
            'Está mapeado manualmente a los URLs'
        ]

        return Response({
            'message': 'Hello World',
            'an_apiview': an_apiview
        })
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [¿Que es una APIView?](08_Que_es_APIView.md) | [Readme](../README.md) | [URL de APIView](10_URL_APIView.md) |
