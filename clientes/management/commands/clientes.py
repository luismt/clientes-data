from django.core.management.base import BaseCommand
import os
from clientes.models import Reporte
from clientes.helpers import Reportfile


class Command(BaseCommand):
    
    def handle(self, *args, **options):
       self.set_params()
       self.file_list=self.get_files_list()
       for file in self.file_list:
           self.engage_reporte(file)

    def engage_reporte(self, file):
        reporte = Reportfile(file) 
        reporte.to_sql()

    def set_params(self):
        self.PWD = os.getcwd()
        self.xls_files = "/xls_files/"
        self.xlsx_files = "/xlsx_files/"
        return

    def get_files_list(self):
        filename_entries = [reporte.filename for reporte in Reporte.objects.all()]
        file_list = os.listdir(self.PWD + self.xls_files)
        return [item for item in file_list if item not in filename_entries]
