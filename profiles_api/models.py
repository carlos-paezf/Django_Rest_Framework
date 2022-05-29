from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Modelo de la base de datos para los usuarios en el sistema """
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Obtener nombre completo """
        return self.name
    
    def get_short_name(self):
        """ Obtener nombre corto """
        return self.name

    def __str__(self):
        """ Retornar cadena representativa del modelo """
        return self.email
