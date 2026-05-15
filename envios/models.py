from django.db import models
from .utils import normalizar_numero_guia


class Guia(models.Model):
    PASOS = [
        (0, 'Envío recogido'),
        (1, 'En Centro Logístico Origen'),
        (2, 'Viajando a destino'),
        (3, 'En Centro Logístico Destino'),
        (4, 'En camino hacia ti'),
        (5, 'Entregado'),
    ]

    numero           = models.CharField(max_length=30, unique=True)
    remitente_nombre = models.CharField(max_length=100)
    remitente_ciudad = models.CharField(max_length=100)
    remitente_depto  = models.CharField(max_length=100, blank=True)
    remitente_dir    = models.CharField(max_length=200, blank=True)
    remitente_tel    = models.CharField(max_length=20, blank=True)

    dest_nombre = models.CharField(max_length=100)
    dest_ciudad = models.CharField(max_length=100)
    dest_depto  = models.CharField(max_length=100, blank=True)
    dest_dir    = models.CharField(max_length=200, blank=True)
    dest_tel    = models.CharField(max_length=20, blank=True)
    dest_peso   = models.CharField(max_length=30, blank=True)
    dest_obs    = models.TextField(blank=True)

    valor          = models.CharField(max_length=50, blank=True)
    empresa        = models.CharField(max_length=100, blank=True)
    paso_actual    = models.IntegerField(choices=PASOS, default=0)
    fecha_creacion    = models.DateTimeField(auto_now_add=True)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Guía'
        verbose_name_plural = 'Guías'

    def save(self, *args, **kwargs):
        self.numero = normalizar_numero_guia(self.numero)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.numero} → {self.dest_nombre} ({self.dest_ciudad})"