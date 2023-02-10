from os import wait
from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "https://vivexux.fullsolutiondns.com/api/onu/get_all_onus_details"
        headers={"X-Token": "2a251f2642474407a2d531ce54823de6"}
        response = requests.get(url, headers=headers)
        onus = response.json().get("onus")
        filt = filter(filter_zone, onus)
        maper = map(convert_onus, filt)
        active_users = [m for m in maper]
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
