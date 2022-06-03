# Crear SuperUsuario

Vamos a crear un Test para el momento de crear un super-usuario:

```py
class ModelTest(TestCase):
    def test_create_new_super_user(self):
        """ > Probar super-usuario creado """
        user = get_user_model().objects.create_superuser('admin@gmail.com', 'admin_1234567890')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
```

Ahora creamos la función para definir el super-usuario dentro de nuestro modelo:

```py
class UserManager(BaseUserManager):
    ...
    def create_superuser(self, email, password):
        super_user = self.create_user(email, password)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using = self._db)

        return super_user
```

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Normalización de Correos](05_Normalizacion_Correos.md) | [Readme](../../README.md) | [Test para listar Usuarios en Django Admin](07_Test_Listar_Usuarios_Django_Admin.md) |
