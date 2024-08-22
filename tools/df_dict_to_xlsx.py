import pandas as pd
from openpyxl.workbook import Workbook 
def df_dict_to_xlsx(dict):
    for key in dict.keys():
        df = dict[key]
        file = key + '.xlsx'
        sheet = key
        df.to_excel(file, sheet_name = sheet)
