from django.db import models


class Reporte(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateField()
    report_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.report_type + "-" + self.filename


    def get_last_date_reportes(self):
        return Reporte.objects.filter(date=Reporte.objects.all().order_by('date').last().date)


class Base(models.Model):
    contrato = models.CharField(max_length=100)
    servicio = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)


    class Meta:
        abstract = True


class ClienteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class SoftvManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reporte__in=Reporte().get_last_date_reportes()).exclude(reporte__report_type__in=['instalado', 'cancelado'])


class ClienteInstaladoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reporte__in=Reporte().get_last_date_reportes()).filter(reporte__report_type__in=['instalado',])

class ClienteCanceladoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reporte__in=Reporte().get_last_date_reportes()).filter(reporte__report_type__in=['cancelado'])

class Cliente(Base):
    objects = ClienteManager()
    softv = SoftvManager()
    instalados = ClienteInstaladoManager()
    cancelados = ClienteCanceladoManager()

class Instalaciones(Base):
    fecha = models.DateField()

class Cancelaciones(Base):
    pass

class FullSolutionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(contrato__in=[c.contrato for c in Cliente.softv.all()])


class FullSolution(models.Model):
    contrato = models.CharField(max_length=100)
    olt_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    audits = FullSolutionManager()
    objects = models.Manager()




from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
