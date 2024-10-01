import pandas as pd
from filehandling.dict_writing import *
def dict_merge(dicts,evidence_table,txt_check):
    '''
    '''
    merged_dict = {}
    k = 0
    b = False
    for dict in dicts:
        
        for key in dict.keys():
            
            if f'Table{k}' == evidence_table:
                k = k + 1
                b = True
                a = merged_dict[evidence_table]
                content = dict[key]
                merged_dict[evidence_table] = pd.concat([a,content],ignore_index=True)
            else:
                
                if b == True:
                    k = k - 1
                    b = False
                
                k = k + 1
                table_name = f'Table{k}'
                content = dict[key]
                merged_dict[table_name] = content
    
    if txt_check == True:
        df_to_txt(merged_dict,'merged_data.txt')

    return merged_dict
