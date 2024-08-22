
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
    
