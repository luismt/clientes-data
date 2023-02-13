import os
from django.core.management.base import BaseCommand
import requests
import pandas as pd

from clientes.models import FullSolution

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('--load', action='append',type=str)

    def handle(self, *args, **options):
        load = options.get("load")
        if load[0] == "api":
            self.resolve_api()
        elif load == "csv":
            self.resolve_csv()

    def resolve_csv(self):
        pwd = os.getcwd()
        csv_dir = "/csv_files/"
        base_df = pd.read_csv(pwd + csv_dir)
        


    def resolve_api(self):
            url = "https://vivexux.fullsolutiondns.com/api/onu/get_all_onus_details"
            headers={"X-Token": "2a251f2642474407a2d531ce54823de6"}
            response = requests.get(url, headers=headers)
            onus = response.json().get("onus")
            filt = filter(filter_zone, onus)
            maper = map(convert_onus, filt)
            active_users = [{"contrato": m} for m in maper]
            fullsolution = FullSolution.objects.bulk_create(
                    FullSolution(source="api", **vals) for vals in active_users
                    )
            print("Active users = ", len(active_users))

def filter_zone(onus):
    if onus.get("zone_name") == "Quattrocom" or onus.get("name") == "ANGEL SANTIAGO UITZIL YAMA":
        return False
    else:
        return True

def convert_onus(onus):
    converted = onus.get("name").split("-")[-2:]
    # return convert
    if len(converted[0]) == 4:
        #print(onus.get("name"))
        return converted[0] + "-" + converted[1]
    else:
        #print(onus.get("name"))
        homoclave = converted[1]
        cuenta = converted[0].split(" ")[-1:][0]
        return cuenta + "-" + homoclave

def convert_name_to_contrato(name: str):
    if name == "VIVEXUX APERTURAS" or name == "DEMETRIO LOPEZ MUKUL":
        return
    converted = name.split("-")[-2:]
    if len(converted[0]) == 4:
        return converted[0] + "-" + converted[1]
    else:
        homoclave = converted[1]
        cuenta = converted[0].split(" ")[-1:][0]
        return cuenta + "-" + homoclave

def get_files_list(self):
    filename_entries = [reporte.filename for reporte in Reporte.objects.all()]
    file_list = os.listdir(self.PWD + self.xls_files)
    return [item for item in file_list if item not in filename_entries]
