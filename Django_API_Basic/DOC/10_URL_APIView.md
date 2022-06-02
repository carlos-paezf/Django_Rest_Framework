# URL de APIView

Vamos a crear un archivo llamado `urls.py` para nuestra app `profiles_api`, en donde cargaremos las urls de nuestro APIView. Ahora, dentro del archivo `profiles_project/urls.py`, importamos la función `include` y registramos las urls de la app `profiles_api`:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('profiles_api.urls'))
]
```

Volvemos al archivo `profiles_api/urls.py`, e importamos la función `path` y las vistas de nuestra app. Creamos el arreglo `urlpatterns` y añadimos un nuevo endpoint para nuestro APIView de prueba. Como no podemos cargar una clase, usamos la función `as_view()` para cargar nuestra configuración como una vista.

```py
from django.urls import path
from profiles_api import views

urlpatterns = [
    path('hello-view/', views.HelloWorldAPIView.as_view())
]
```

Para comprobar los cambios ingresamos a la URL `http://127.0.0.1:8000/api/hello-view`, y podemos observar una interfaz que contiene la respuesta que retornamos en el método `get()` de la clase `HelloWorldAPIView`.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Creando primer APIView](09_Creando_Primer_APIView.md) | [Readme](../README.md) | [Crear Serializador](11_Crear_Serializador.md) |
