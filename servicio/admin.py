from django.contrib import admin
from servicio.models import Pendientes


class PendientesAdmin(admin.ModelAdmin):
    list_display = ["orden", "contrato", "cliente", "fecha", "servicio", "reporte"]


admin.site.register(Pendientes, PendientesAdmin)
