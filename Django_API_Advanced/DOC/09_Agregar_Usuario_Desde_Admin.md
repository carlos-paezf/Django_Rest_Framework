# Agregar Usuario desde Admin

Vamos a `core/tests/test_admin.py` y creamos un nuevo test para saber si se está renderizando de manera correcta la página de administración de usuario:

```py
class AdminSiteTest(TestCase):
    ...
    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
```

Como sabemos, al momento de estar desarrollando bajo el principio de TDD, la prueba va primero y va a fallar, por lo tanto luego implementamos la lógica y "esperamos" que funcione el test. En nuestro caso, para hacer que el test pase, vamos a añadir la siguiente tupla a la clase `UserAdmin` del archivo `core/admin.py`:

```py
class UserAdmin(BaseUserAdmin):
    ...
    add_fieldsets = (
        (None,
            {
                'classes': ('wide', ),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
```

> El comando para ejecutar los test es:
>
> ```txt
> python manage.py test
> ```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
|  [Modificar Django Admin para cambiar Modelo de Usuario](08_Modificar_Django_Admin_Para_Cambiar_Modelo_User.md) | [Readme](../../README.md) | [Crear App de Usuarios](10_Crear_App_Usuarios.md) |
