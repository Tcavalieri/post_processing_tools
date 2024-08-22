import io
import pandas as pd
from txt_reading import txt_reading
from df_dict_to_txt import df_dict_to_txt
from df_dict_to_xlsx import df_dict_to_xlsx

def lammps_log_parsing(file_name):
    """
    This function read a lammps log file, extract the tables with properties, store them in a dict and print them in a txt file.
    Parameters:
    file_name (str): 'log.lammps'. the function is optimized for this file. 
    Return: 
    tables_dict (dict): dictionary with all the tables in the log as pandas dataframes.
    requirments:
    txt_reading
    df_dict_to_txt
    """
    
    cf = txt_reading(file_name)

    # initialization of a loop to determine the start and end of each table with the relevant data
    start = []
    end = []

    for i in range(len(cf)):
        a = cf[i].split()
        if a[:4] == ['Per','MPI','rank','memory']: # key sentence for finding the start of a table from log.lammps files
            n = i
            start.append(n)
        if a[:3] == ['Loop','time', 'of']: # key sentence for finding the end of a table from log.lammps files
            k = i
            end.append(k)
    

    # initialization of the dictionary that stores every table of data
    tables_dict = {}
    tables_keys = [0]*len(start)

    for i in range(len(start)):
        tables_keys[i] = 'Table' + str(i+1) # creation of the dictionary's keys with progressive numbers
        string_list = cf[start[i]+1:end[i]] # slicing of main file (i+1 is needed to exclude the key sentence used to find the table)
        tables_dict[tables_keys[i]] = pd.read_csv(io.StringIO('\n'.join(string_list)), sep='\s+') # creation of each dataframe througth the creation of a csv file (sep='\s+' tell that the delimiter is a white space)

    # creation of a txt file to store the dictionary of dataframes
    df_dict_to_txt(tables_dict,'data_tables.txt')       
    # creation of a txt file to store the dictionary of dataframes
    df_dict_to_xlsx(tables_dict)
    
    return tables_dict

