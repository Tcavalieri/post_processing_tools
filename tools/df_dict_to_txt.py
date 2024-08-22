
def df_dict_to_txt(dict,file_name):
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