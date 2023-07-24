"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.IntegerField(null=True, blank=True)
    leaving_date = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tratamiento(models.Model):
    """Tratamiento object."""
    codigo = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    duracion_minutos = models.IntegerField()
    familia = models.CharField(max_length=2, blank=True, null=True)
    precio_base = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre