# Actualización de Contraseña y Login de Usuario

Cuando actualizamos los datos del usuario, tenemos en mente que la contraseña se debe guardar en un hash, pero actualmente se está actualizando como texto plano. Esto ocurre por que el override del comportamiento predeterminado de Django Rest Framework, el cual se encuentra en `ModelSerializer`, no está actualizando, por lo tanto debemos agregar un nuevo método dentro de nuestra clase `UserProfileSerializer`. Si la data validada contiene una contraseña, entonces se remueve de dicho objeto y se modifica la contraseña en una instancia que es llamada por el método `update()` de la superclase `ModelSerializer`:

```py
class UserProfileSerializers(serializers.ModelSerializer):
    ...
    def update(self, instance, validated_data):
        """ Actualiza la cuenta del usuario """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Serializar perfil de usuario](19_Serializar_Perfil_Usuario.md) | [Readme](../README.md) | [Crear perfiles ViewSet](20_Actualización_Password_Login_Usuario.md) |
