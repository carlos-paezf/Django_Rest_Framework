from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from profiles_api import serializers, models, permissions


class HelloWorldAPIView(APIView):
    """ APIView de prueba """
    serializer_class = serializers.HelloWorldSerializers

    def get(self, request, format=None):
        """ Retornar lista de caracteristicas del APIView """
        an_apiview = [
            'Usamos métodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional de Django',
            'Nos da el mayor control sobre la lógica de nuestra aplicación',
            'Está mapeado manualmente a los URLs'
        ]

        return Response({
            'message': 'Hello World',
            'an_apiview': an_apiview
        })

    def post(self, request):
        """ Crear un mensaje con nuestro nombre """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'message': message
            })
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Actualizar un objeto """
        return Response({ 'method': 'PUT' })

    def patch(self, request, pk=None):
        """ Actualizar parcialmente un objeto """
        return Response({ 'method': 'PATCH' })

    def delete(self, request, pk=None):
        """ Eliminar un objeto """
        return Response({ 'method': 'DELETE' })


class HelloWorldViewSet(viewsets.ViewSet):
    """ Test API ViewSet """
    serializer_class = serializers.HelloWorldSerializers

    def list(self, request):
        """ Retornar un mensaje """
        a_viewset = [
            'Usa acciones como list, create, retrieve, update, partial_update, delete'
            'Automáticamente mapea a los URLs usando Routers',
            'Provee más funcionalidad con menos código'
        ]

        return Response({
            'message': 'Hola',
            'a_viewset': a_viewset
        })

    def create(self, request):
        """ Crear un nuevo mensaje """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola mundo {name}'

            return Response({ 'message': message })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Obtener un objeto y su id """
        return Response({ 'http_method': 'GET' })

    def update(self, request, pk=None):
        """ Actualizar un objeto """
        return Response({ 'http_method': 'PUT' })

    def partial_update(self, request, pk=None):
        """ Actualizar parcialmente un objeto """
        return Response({ 'http_method': 'PATCH' })

    def destroy(self, request, pk=None):
        """ Eliminar un objeto """
        return Response({ 'http_method': 'DELETE' })


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Maneja la creación y actualización de perfiles """
    serializer_class = serializers.UserProfileSerializers
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """ Crear tokens de autenticación del usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Crear, Leer, y actualizar el profile feed """
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializers
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """ Setear el perfil de usuario para el user logeado """
        serializer.save(user_profile = self.request.user)
