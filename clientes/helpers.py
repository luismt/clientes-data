import os
from typing import Any
from xls2xlsx import XLS2XLSX
from openpyxl import load_workbook
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

from clientes.models import Cancelaciones, Cliente, Instalaciones, Reporte
from servicio.models import Pendientes


def convert_to_xlsx(file_name):
    xls_dir = "/xls_files/"
    xlsx_dir = "/xlsx_files/"
    xls = XLS2XLSX(os.getcwd() + xls_dir + file_name)
    xlsx_file = xls.to_xlsx(os.getcwd() + xlsx_dir + file_name + "x")
    return xlsx_file

def get_base_df(file_path):
    wb = load_workbook(file_path)
    ws = wb["Sheet1"]
    base_df = pd.DataFrame(ws.values)
    return base_df

def get_pd_filt(df: pd.DataFrame, str_pattern: str):
    return df.apply(lambda r: r.astype('string').str.contains(str_pattern).any(), axis=1)

def get_reporte_name(df: pd.DataFrame):
    options = ['Supendidos', 'Desconectados', 'corriente', 'Adelantados', 'Cortesía', 'Instalado', 'Cancelado']
    for option in options:
        filt = get_pd_filt(df, option)
        row_labels = df[filt]
        if len(row_labels):
            return option.lower()
        
def get_date(df: pd.DataFrame):
    rows = len(df)
    columns = len(df.columns)
    for row in range(0, rows):
        for column in range(0, columns):
            if type(df.loc[row, column]) == Timestamp:
                return df.loc[row, column]
            
def drop_columns(df: pd.DataFrame, columns):
    df = df.drop(columns=columns)
    return df

def squezze_contrato(df: pd.DataFrame):
    str_pattern = "Contrato"
    filt = (df.apply(lambda r: r.astype("string").str.contains(str_pattern).any(), axis=1))
    row_labels = df[filt]
    c_range = row_labels.index[0]
    c_range = int(float(c_range)) + 1
    for i in range(0, c_range):
        df.drop(i, inplace=True)
    df.dropna(inplace=True)
    return df


class Reportefile:
    reporte_name: Any
    df: pd.DataFrame
    columns_to_drop = {
        "corriente": [0, 2, 3, 4, 5, 6,7,9,10, 11, 12,13, 14, 15,16,18,19, 20, 21, 22],
        "desconectados": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19],
        "supendidos": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19],
        "adelantados": [0, 2, 3, 4, 5, 6,7,9,10, 11, 12,13, 14, 15,16,18,19, 20, 21, 22],
        "cortesía": [0,2, 3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "instalado": [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 14, 15, 16, 17, 18],
        "cancelado": [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18],
        "pendientes": [0, 2, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16],
    }
    
    columns_to_rename = {
        "corriente": ["contrato", "servicio", "periodo"],
        "desconectados": ["contrato", "servicio", "periodo"],
        "supendidos":["contrato", "servicio", "periodo"],
        "adelantados": ["contrato", "servicio", "periodo"],
        "cortesía": ["contrato", "servicio"],
        "instalado": ["contrato", "servicio", "fecha", "periodo"],
        "cancelado": ["contrato", "servicio", "periodo"],
        "pendientes": ["orden", "contrato", "cliente", "fecha", "servicio"],
    }

    db_classes = {
        "corriente": Cliente,
        "desconectados": Cliente,
        "supendidos":Cliente,
        "adelantados": Cliente,
        "cortesía": Cliente,
        "instalado": Instalaciones,
        "cancelado": Cancelaciones,
        "pendientes": Pendientes,
    }
    
    def __init__(self, filename):
        self.filename = filename
        
    def to_sql(self):
        self.xlsx_file = convert_to_xlsx(self.filename)
        self.base_df = get_base_df(self.xlsx_file)
        self.date = get_date(self.base_df)
        self.reporte_name = get_reporte_name(self.base_df)
        self.df = drop_columns(self.base_df, self.columns_to_drop.get(self.reporte_name))
        if self.reporte_name != "cortesía":
            self.df = squezze_contrato(self.df)
        else:
            self.df.dropna(inplace=True)
        self.df.columns = self.columns_to_rename.get(self.reporte_name)
        filename = self.filename + "x"
        self.reporte = Reporte(filename=filename, date=self.date, report_type=self.reporte_name)
        self.reporte.save()
        self.create_entries(self.df, self.reporte)

    def create_entries(self, df, reporte):
        self.db_classes.get(self.reporte_name).objects.bulk_create(
                self.db_classes.get(self.reporte_name)(reporte=reporte, **vals) for vals in df.to_dict("records")
                )

def get_audited_list():
    filename = "google_drive/Clientes a compartir - Revision.csv"
    base_df = pd.read_csv(filename)
    records_dict = base_df.to_dict("records")
    records_list = [item.get("contrato") for item in records_dict]
    return records_list
