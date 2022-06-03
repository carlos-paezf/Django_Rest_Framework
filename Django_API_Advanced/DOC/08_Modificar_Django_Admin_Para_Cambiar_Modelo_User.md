# Modificar Django Admin para cambiar Modelo de Usuario

Creamos un nuevo test para comprar que la url `/admin/core/user/<id_user>`, este cambiando de manera adecuada.

```py
class AdminSiteTest(TestCase):
    ...
    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
```

Para lograr que pase el test vamos a ir a `core/admin.py` y haremos la siguiente modificación a la clase `UserAdmin`:

```py
...
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ...
    fieldsets = (
        (None,
            {
                'fields': ('email', 'password')
            }
        ),
        (_('Personal Info'),
            {
                'fields': ('name', )
            }
        ),
        (_('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important Dates'),
            {
                'fields': ('last_login', )
            }
        )
    )
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Test para listar Usuarios en Django Admin](07_Test_Listar_Usuarios_Django_Admin.md) | [Readme](../../README.md) | [Agregar Usuario desde Admin](09_Agregar_Usuario_Desde_Admin.md) |
