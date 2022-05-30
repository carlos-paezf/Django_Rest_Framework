from rest_framework import serializers


class HelloWorldSerializers(serializers.Serializer):
    """ Serializar un campo para probar nuestro APIView """
    name = serializers.CharField(max_length = 10)
