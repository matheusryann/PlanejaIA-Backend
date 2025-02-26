from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    # Resolvendo conflitos com auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_set',  # Evita conflito com o modelo padrão do Django
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_permissions_set',  # Evita conflito
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
