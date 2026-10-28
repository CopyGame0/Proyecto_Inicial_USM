from django.conf import settings
from django.db import models

class RecetaGuardada(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # si se borra el usuario, se borran sus recetas
        related_name='recetas',
    )
    id_externo = models.CharField(max_length=50)   # id que entrega la API de recetas
    titulo = models.CharField(max_length=200)
    imagen = models.URLField(blank=True)
    calorias = models.FloatField(null=True, blank=True)
    proteina = models.FloatField(null=True, blank=True)
    carbohidratos = models.FloatField(null=True, blank=True)
    azucar = models.FloatField(null=True, blank=True)
    guardada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'id_externo')   # no guardar la misma receta dos veces

    def __str__(self):
        return f'{self.titulo} ({self.usuario})'