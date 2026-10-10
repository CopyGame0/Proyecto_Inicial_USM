from django.db import models
from django.contrib.auth.models import AbstractUser

#Perfiles de usuarios
class Perfil(AbstractUser):
    pauta_nutricional = models.TextField(
        blank=True,
        null=True,
        help_text="Pauta nutricional del usuario"
    )
    edad = models.PositiveIntegerField(blank=True, null=True)
   
    def __str__(self):
        return f"{self.username} ({self.email})"