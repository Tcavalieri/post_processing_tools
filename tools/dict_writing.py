import pandas as pd
from openpyxl.workbook import Workbook 

def df_to_xlsx(dict):
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

def df_to_txt(dict,file_name):
    """
    This function write the pandas dataframes in a dictionary to a txt file.
    parameters:
    dict (dict): dictionary of dataframes.
    file_name (str): name of the txt file which will be created ('name.extension').
    """   
    with open(file_name, 'w') as f:
        for key in dict.keys():
            f.write('\n'+'='*40 +'\n')
            f.write(key)
            f.write('\n'+'='*40 +'\n')
            f.write(dict[key].to_string(header=True, index=True))
        f.close()
