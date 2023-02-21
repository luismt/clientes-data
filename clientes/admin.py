from django.contrib import admin
from clientes.models import Cliente, Reporte, FullSolution 

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['filename', 'date', 'report_type',]

admin.site.register(Cliente)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(FullSolution)
