from os import getcwd, wait
from .models import Atrasado, Reporte
from openpyxl import load_workbook, Workbook
from xls2xlsx import XLS2XLSX
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import numpy as np

class Reportfile:

    upload_authorized = False

    def __init__(self, filename):
        self.filename = filename
        self.PWD = getcwd() 
        self.check_db()

        
    def check_db(self):
        if self.filename in [reporte for reporte in Reporte.objects.all()]:
            raise Exception("file alraedy in database")
        else:
            self.upload_authorized = True

    def to_sql(self):
        xlsx = self.convert_to_xlsx()
        base_df = self.get_base_df(xlsx)
        timestamp = self.get_timestamp(base_df)
        name = self.get_reporte_name(base_df)
        self.clean_df(base_df)
        reporte = Reporte(filename=self.filename, date=timestamp, report_type=name)
        reporte.save()

        self.create_entries(self.df, reporte)

    def convert_to_xlsx(self):
        xls_file = XLS2XLSX(self.PWD + "/xls_files/" + self.filename)
        return xls_file.to_xlsx(self.PWD + "/xlsx_files/" + self.filename + "x")

    def get_base_df(self, xlsx_path):
        wb = load_workbook(xlsx_path)
        ws = wb["Sheet1"]
        base_df = pd.DataFrame(ws.values)
        return base_df

    def get_timestamp(self, base_df):
        rows = len(base_df)
        columns = len(base_df.columns)
        for row in range(0, rows):
            for column in range(0, columns):
                if type(base_df.loc[row, column]) == Timestamp:
                    return base_df.loc[row, column]

    def get_reporte_name(self, base_df):
        options = ['Supendidos', 'Desconectados',]
        for option in options:
            filt = get_pd_filt(base_df, option)
            row_labels = base_df[filt]
            if len(row_labels):
                return option.lower()

    def clean_df(self, base_df):
        self.df = self.drop_columns_rows(base_df)
        self.rename_columns()
        return

    def drop_columns_rows(self, base_df):
        df = base_df.drop(columns=[0,2,4,5,7,9,10,12,13,16,19])
        str_pattern = "Contrato" # search for patttern Contrato cell
        
        filt = (df
                .apply(lambda r: r.astype('string').str.contains(str_pattern)
                    .any(), axis=1))
        row_labels =df [filt]
        c_range = row_labels.index[0]
        c_range = int(float(c_range)) + 1

        for i in range(0, c_range):
            df.drop(i, inplace=True)
        df.dropna(inplace=True)
        return df

    def rename_columns(self):
        column_names = ['contrato', 'nombre', 'mes', 'year', 'servicio', 'monto', 'celular', 'periodo', 'distribuidor']
        self.df.columns = column_names
        self.df.dropna(inplace=True)
        self.df = self.df.astype({"year": 'int'})
        return

    def create_entries(self, df, reporte):
        Atrasado.objects.bulk_create(
                Atrasado(reporte=reporte, **vals) for vals in df.to_dict("records")
                )

    def check_authorized_upload(self):
        if not self.upload_authorized:
            raise Exception("Already in database")


def get_pd_filt(df: pd.DataFrame, str_pattern: str):
    return (df.apply(lambda r: r.astype('string').str.contains(str_pattern).any(), axis=1))
