# Área de Login

Para permitir el ingreso del usuario, requerimos de que nos entregue un token, por tal motivo debemos importar los siguientes elementos desde `rest_framework`:

```py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
```

Luego, creamos una clase que hereda de `ObtainAuthToken`, en la que nos encargamos de crear los token de usuario. Lo primero será añadir las clases de renderizado por defecto, las cuales traemos de `api_settings`

```py
class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
```

Vamos a `profile_api/urls.py` y añadimos una nueva ruta:

```py
urlpatterns = [
    ...,
    path('login/', views.UserLoginApiView.as_view()),
    ...
]
```

Ingresamos a la URL `http://127.0.0.1:8000/api/login` y ponemos nuestras credenciales en el formulario. Recordemos que en vez de Username tenemos nuestro correo. Cuando todo va bien, tenemos una respuesta con un token.

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Filtrar Usuarios](24_Filtrar_Usuarios.md) | [Readme](../../README.md) | [API para Feed de perfil de Usuario](26_API_Feed_Perfil_Usuario.md) |
