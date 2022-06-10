from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        """ Crear y guardar un nuevo usuario """
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password):
        """ Crear superuser """
        super_user = self.create_user(email, password)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using = self._db)

        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de Usuario que soporta hacer Login con Email en vez de username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Modelo del Tag para la receta """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Modelo del Ingrediente para la receta """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name