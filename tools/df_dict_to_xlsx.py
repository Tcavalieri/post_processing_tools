import pandas as pd
from openpyxl.workbook import Workbook 
def df_dict_to_xlsx(dict):
    """
    This function write the pandas dataframes in a dictionary to a .xlsx file.
    parameters:
    dict (dict): dictionary of dataframes.
    """   
    for key in dict.keys():
        df = dict[key]
        file = key + '.xlsx'
        sheet = key
        df.to_excel(file, sheet_name = sheet)
