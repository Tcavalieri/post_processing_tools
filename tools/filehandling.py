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

def txt_reading(file_name):    
    """
    this function read a given txt file as a whole (suitable for not too big file).
    parameters:
    file_name (str): name of the txt file.
    Returns:
    read_file (list): list of strings each of them are a line of the original txt file.
    """
    # read a txt file and extract each line (including blank lines) converting them into strings: 
    # the result is a list of strings
    with open(file_name) as f:
        read_file = f.readlines()
       
    # this operation remove every character '\n' (a blank line that follows)
    read_file = [x.strip() for x in read_file]    
    # this operation remove extra white spaces in each element and return strings with only one blank space
    # as delimiter
    read_file = [' '.join(x.split()) for x in read_file]

    return read_file    

def dict_merge(dicts,evidence_table,txt_check):
    '''
    function for the creation of a dictionary of tables by merging two incomplete dictionary (used especially after restart of an interrupted simulation).
    Parameters:
    dicts (list): list of dictionary that you want to merge.
    evidence_table (str): the name o f the incomplete table present in both the incomplete dictionaries. The merging point.
    txt_check (boolean): boolean that if True will create a txt file of the merged dict.
    Return:
    merged_dict (dict): dictionary of pandas dataframes (tables with the data of the simulation).
    '''
    # initialisation of the merged dict
    merged_dict = {}
    k = 0
    b = False

    # loop for the two dicts you want to be merged together
    for dict in dicts:
        
        # loop that goes through all the tables present in each dict
        for key in dict.keys():
            
            # if the table of the second dict is the one incomplete will be merged with the last table of the first dict.
            if f'Table{k}' == evidence_table:
                k = k + 1
                b = True
                a = merged_dict[evidence_table]
                content = dict[key]
                merged_dict[evidence_table] = pd.concat([a,content],ignore_index=True)
            else:
                # this conditional handle the enumeration of the tables after the merging to not skip number
                if b == True:
                    k = k - 1
                    b = False
            # this store each table in a new dictionary that will be the final merged one    
                k = k + 1
                table_name = f'Table{k}'
                content = dict[key]
                merged_dict[table_name] = content
    # conditional that handle the printing of a txt file with the results.
    if txt_check == True:
        df_to_txt(merged_dict,'merged_data.txt')

    return merged_dict

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
    # initialisation
    n = 0
    k = 0
    i = 0
    a = False

    file = []

    # main loop
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
    
    # this if statement is to handle cases in witch the last table is incomplete because of a crash of the programm
    if len(init)-1 == len(fin):
        fin.append(len(file))
    
    # initialization of the dictionary that stores every table of data
    tables_dict = {}
    tables_keys = [0]*len(init)

    for i in range(len(init)):
        tables_keys[i] = 'Table' + str(i+1) # creation of the dictionary's keys with progressive numbers
        string_list = file[init[i]+2:fin[i]] # slicing of main file (i+2 is needed to exclude the key sentence used to find the table and the header with the name of the properties)
        intermidiate = pd.DataFrame(string_list, columns=file[init[i]+1]) # the init[i]+1 is needed to give the header for the creation of the columns name in the dataframe
        tables_dict[tables_keys[i]] = intermidiate.astype(float, errors='ignore') # this is used to convert data from string to float

    if txt_check == True:
        # creation of a txt file to store the dictionary of dataframes
        df_to_txt(tables_dict,'data_tables.txt')       
    if xlsx_check == True:
        # creation of a txt file to store the dictionary of dataframes
        df_to_xlsx(tables_dict)

    return tables_dict