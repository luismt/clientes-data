from django.db import models

from clientes.models import Reporte

class Pendientes(models.Model):
    orden = models.IntegerField()
    contrato = models.CharField(max_length=100)
    servicio = models.CharField(max_length=255)
    fecha = models.DateField()
    cliente = models.CharField(max_length=100)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)

