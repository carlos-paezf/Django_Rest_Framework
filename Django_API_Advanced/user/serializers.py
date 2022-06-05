from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """ Crear un nuevo usuario con la clave encriptada y retornarlo """
        return get_user_model().objects.create_user(**validated_data)
