# Test para listar Usuarios en Django Admin

Vamos a crear un nuevo archivo llamado `core/tests/test_admin.py` y dentro tenemos una clase con una función para configurar de manera inicial el inicio de sesión forzado del super-usuario. Luego tenemos una función para listar los usuarios que se encuentren en nuestro módulo de usuarios:

```py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser('admin@admin.com', 'admin_1234567890')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user('test@test.com', 'test', name='Test User')

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
```

Ahora vamos al archivo `core/admin.py` y creamos una clase para la administración de los usuarios, la cual se usa al momento de registar el modelo de `User`:

```py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Crear SuperUsuario](06_Crear_SuperUser.md) | [Readme](../../README.md) | [Modificar Django Admin para cambiar Modelo de Usuario](08_Modificar_Django_Admin_Para_Cambiar_Modelo_User.md) |
