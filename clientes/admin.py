from django.contrib import admin
from clientes.models import Cliente, Reporte, FullSolution, Instalaciones, Cancelaciones, Contrataciones

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['filename', 'date', 'report_type',]
    ordering = ['-date']

class BaseAdmin(admin.ModelAdmin):
    list_display = ["contrato","servicio", "periodo", "reporte",]

class DateBaseAdmin(BaseAdmin):
    list_display = ["contrato","servicio", "periodo", "fecha", "reporte",]

admin.site.register(Cliente, BaseAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(FullSolution)
admin.site.register(Instalaciones, DateBaseAdmin )
admin.site.register(Cancelaciones, BaseAdmin )
admin.site.register(Contrataciones, DateBaseAdmin )
