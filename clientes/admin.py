from django.contrib import admin
from clientes.models import Cliente, Reporte, FullSolution, Instalaciones, Cancelaciones

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['filename', 'date', 'report_type',]
    ordering = ['-date']

class InstalacionesAdmin(admin.ModelAdmin):
    list_display = ["contrato","servicio", "fecha"]

class ClientesAdmin(admin.ModelAdmin):
    list_display = ["contrato", "servicio", "periodo"]

class CancelacionesAdmin(admin.ModelAdmin):
    list_display = ["contrato", "servicio", "periodo"]

admin.site.register(Cliente, ClientesAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(FullSolution)
admin.site.register(Instalaciones, InstalacionesAdmin )
admin.site.register(Cancelaciones, CancelacionesAdmin)
