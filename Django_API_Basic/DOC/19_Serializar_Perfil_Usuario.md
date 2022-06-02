# Serializar perfil de usuario

Dentro de nuestro archivo `profiles_api/serializers.py`, vamos a importar nuestros modelos, con el fin de basar nuestros serializadores en ellos. Teniendo este objetivo en mente, creamos una nueva clase que va a heredar de la clase `ModelSerializer`, y dentro de nuestra clase creamos otra clase llamada `Meta` para definir el modelo a usar, los campos que necesitamos, y las configuraciones extras que requerimos (en este caso queremos que la contraseña solo sea accesible al momento de crear el usuario, en los demás casos de muestra en un estilo de asteriscos `*`).

```py
from rest_framework import serializers
from profiles_api import models

...

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
```

El siguiente paso es sobrescribir la función de crear un usuario, por lo que creamos una función en la que tenemos un usuario retornado de la función `create_user()`, a la cual se la pasan por parámetros los datos validados.

```py
class UserProfileSerializers(serializers.ModelSerializer):
    ...
    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
```

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [API para perfil de usuario](18_API_Perfil_Usuario.md) | [Readme](../../README.md) | [Actualización de Contraseña y Login de Usuario](20_Actualización_Password_Login_Usuario.md) |
