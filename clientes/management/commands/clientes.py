from django.core.management.base import BaseCommand
import os
from clientes.models import Reporte
from clientes.helpers import Reportefile


class Command(BaseCommand):
    
    def handle(self, *args, **options):
       self.set_params()
       self.file_list=self.get_files_list()
       stop = 0
       print(stop)
       for file in self.file_list:
           self.engage_reporte(file)

    def engage_reporte(self, file):
        reporte = Reportefile(file) 
        reporte.to_sql()

    def set_params(self):
        self.PWD = os.getcwd()
        self.xls_files = "/xls_files/"
        self.xlsx_files = "/xlsx_files/"
        return

    def get_files_list(self):
        filename_entries = [reporte.filename[:-1] for reporte in Reporte.objects.all() if Reporte.objects.all().count() > 0]
        file_list = os.listdir(self.PWD + self.xls_files)
        if ".DS_Store" in file_list:
            file_list.remove(".DS_Store")
        return [item for item in file_list if item not in filename_entries]
