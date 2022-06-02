# Agregar URL Router

Los ViewSets no son llamados en las rutas tal como lo hicimos con el APIView, en este caso requerimos de la clase `DefaultRouter`, la cual importamos del módulo `routers` de `rest_framework`. Luego definimos una instancia de dicha clase, y registramos un endpoint base para la clase `HelloWorldViewSet`. Dentro del arreglo de `urlpatterns`, registramos la instancia que acabamos de configurar:

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloWorldViewSet, basename = 'hello-viewset')

urlpatterns = [
    ...,
    path('', include(router.urls))
]
```

Para probar nuestro ViewSet, ingresamos a la ruta `http://127.0.0.1:8000/api` y podremos observar que la interfaz cambio un poco, puesto que ahora solo aparece la ruta `hello-viewset` dentro de la respuesta, la cual nos retorna la respuesta que definimos en el método `list()` en la vista.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Crear un ViewSet](15_Crear_ViewSet.md) | [Readme](../../README.md) | [Creando RetrieveUpdate, PartialUpdate y Destroy](17_Creando_RetrieveUpdate_PartialUpdate_Destroy.md) |
