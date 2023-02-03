from django.db import models


class Reporte(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateField()
    report_type = models.CharField(max_length=255)


class Base(models.Model):
    contrato = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    mes = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    servicio = models.CharField(max_length=100)
    monto = models.CharField(max_length=100)
    celular = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    distribuidor = models.CharField(max_length=100)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)


    class Meta:
        abstract = True


class Atrasado(Base):
    pass

from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

