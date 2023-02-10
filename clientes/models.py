from django.db import models


class Reporte(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateField()
    report_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Base(models.Model):
    contrato = models.CharField(max_length=100)
    servicio = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)


    class Meta:
        abstract = True


class Cliente(Base):
    pass

class FullSolution(models.Model):
    contrato = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

