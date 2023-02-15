from django.urls import path
from clientes.views import create_track, index, reporte_list, audits_to_csv

app_name = 'clientes'

urlpatterns = [
        path('create/', create_track, name='create_track'),
        path('', reporte_list, name='reporte_list'),
        path('audits/', audits_to_csv, name='audits_csv'),
        ]

