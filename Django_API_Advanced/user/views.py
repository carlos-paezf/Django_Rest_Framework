from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Crear nuestro usuario en el sistema """
    serializer_class = UserSerializer
