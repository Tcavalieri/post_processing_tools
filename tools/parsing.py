import pandas as pd
from filehandling.dict_writing import *

def parsing(file_name,init_key,fin_key,txt_check,xlsx_check):
    '''
    This function read a txt file line by line and parse the information inside it based on key_sentences provided by the user and return a dict of dataframe, is txt version and xlsx files.
    Parameters:
    file_name (string): the name of the file object of the parsing procedure. is a string.
    init_key (list of string): key sentence for the beginning of the section of interest. for lammps log is ['Per','MPI','rank','memory'].
    fin_key (list of string): key sentence for the end of the section of interest. for lammps log is ['Loop','time','of'].
    txt_check (boolean): if True create a txt file with the results.
    xlsx_check (boolean): if True create multiple (as the number of tables) xlsx file with the results.
    Return:
    tables_dict (dict): dictionary of dataframe.

    '''
    n = 0
    k = 0
    i = 0
    a = False

    file = []

    with open(file_name) as f:
        while True:
        
            readfile = f.readline()
            if not readfile:
                break
            readfile = readfile.strip()
            readfile = readfile.split()
            n = n + 1

            if readfile[:4] == init_key: # key sentence for finding the start of a table from log.lammps files
                file.append('Begin Table')
                k = n
                a = False
        
            if readfile[:3] == fin_key: # key sentence for finding the end of a table from log.lammps files
                file.append('End Table')
                a = True
        
            if a == True:
                k = n + 1
        
            if k == 0:
                continue
            elif k >= n:
                continue
            elif k < n:
                file.append(readfile)

    init = []
    fin = []

    for i in range(len(file)):
        if file[i] == 'Begin Table':
            nn = i
            init.append(nn)
        if file[i] == 'End Table':
            kk = i
            fin.append(kk)
    # initialization of the dictionary that stores every table of data
    tables_dict = {}
    tables_keys = [0]*len(init)

    for i in range(len(init)):
        tables_keys[i] = 'Table' + str(i+1) # creation of the dictionary's keys with progressive numbers
        string_list = file[init[i]+2:fin[i]] # slicing of main file (i+2 is needed to exclude the key sentence used to find the table and the header with the name of the properties)
        intermidiate = pd.DataFrame(string_list, columns=file[init[i]+1]) # the init[i]+1 is needed to give the header for the creation of the columns name in the dataframe
        tables_dict[tables_keys[i]] = intermidiate.astype(float, errors='ignore')

    if txt_check == True:
        # creation of a txt file to store the dictionary of dataframes
        df_to_txt(tables_dict,'data_tables.txt')       
    if xlsx_check == True:
        # creation of a txt file to store the dictionary of dataframes
        df_to_xlsx(tables_dict)

    return tables_dict
