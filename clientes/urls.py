from django.urls import path
from clientes.views import create_track, index, reporte_list

app_name = 'clientes'

urlpatterns = [
        path('create/', create_track, name='create_track'),
        path('', reporte_list, name='reporte_list'),
        ]

