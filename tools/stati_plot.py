import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from filehandling.dict_writing import *
from units_dict import units
import math

def stati_plot(dict,txt_check,e_electro):
    '''
    Function that create a dictionary of dataframe with the property as columns and the mean and std for each table(step) in it (dataframe). It also plots the results.
    Parameters:
    dict (dict): a dictionary o dataframe with in it tables (step) as columns with in it all the relevant statistics for all the properties (dataframe).
    txt_check (boolean): if True it creates a txt file with all the results.
    e_electro (boolean): if True it creates a new entry for the total electrostatic energy.
    '''
    # initialisation (to be improved)
    property_summary ={}
    prop_list = dict['Table2_properties']['Property'] # extract the list of properties in a table: TotEng, KinEng,...etc.
    dict_aux ={}
    
    # auxiliary dictionary for creation of the dataframes with average and standard deviation for the same 
    # property in each step of equilibration procedure
    dict_aux['Tables'] = []
    
    # index for finding the meaningful table: NpT sim at the end of a step
    index = 1
    ind = [index]
    
    # calculation of the index
    while index < len(dict.keys())-1:
        index = index + 3
        ind.append(index)
    
    # creation of the dataframe entry Tables for organizing the property data in each table in a single dataframe
    for k in range(len(dict.keys())):
        dict_aux['Tables'].append(f'Table_{k+2}')
    
    # loop for finding the relevant value for each property in each table and storing them
    for n in range(len(prop_list)):
        
        ave = [] # list of averaged values
        std = [] # list of standard deviation values
        for key in dict.keys():
            df = dict[key]
            
            ave.append(df.iloc[n]['Average'])
            std.append(df.iloc[n]['Standard Deviation'])
        
        dict_aux['Average'] = ave
        dict_aux['Standard Deviation'] = std
        property_summary[prop_list[n]] = pd.DataFrame(dict_aux) # creation of the dataframes for each new table of average and stand. dev values
    # conditional and related loop for the calculation of the averaged total electrostatic energy and its standard deviation    
    if e_electro == True:
        ave_el = []
        std_el = []
        for key in dict.keys():
            df_el = dict[key]
            ave_el.append(df_el.iloc[8]['Average'] + df_el.iloc[9]['Average'])
            std_el.append(math.sqrt((df_el.iloc[8]['Standard Deviation'])**2 + (df_el.iloc[9]['Standard Deviation'])**2))
        dict_aux['Average'] = ave_el
        dict_aux['Standard Deviation'] = std_el
        property_summary['E_electro'] = pd.DataFrame(dict_aux)
        
    # extraction of the Temperature values in the relevant step (NpT after ramp) for the plots
    temp = []
    temp_std = []
    for i in ind:
        temp.append(property_summary['Temp'].iloc[i]['Average'])
        temp_std.append(property_summary['Temp'].iloc[i]['Standard Deviation'])
    temp = np.array(temp)
    temp_std = np.array(temp_std)

    # loop for the creation of the plots to see the behaviour through the steps
    for key in property_summary.keys():
        y = []
        y_err = []
        for i in ind:
            y.append(property_summary[key].iloc[i]['Average'])
            y_err.append(property_summary[key].iloc[i]['Standard Deviation'])
        y = np.array(y)
        y_err = np.array(y_err)
        # creation of the file to store the figure
        file = key + '_' + 'Temp' + '.jpg'
        # includes error bars
        plt.errorbar(temp,y,yerr=y_err,xerr=temp_std,ecolor='tab:orange',capsize=2)
        plt.xlabel('Temp (K)')
        plt.ylabel(units[key])
        plt.title(key)
        plt.grid(True)
        plt.savefig(file,bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
        plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!
    
    # check for printing the results also in a txt file
    if txt_check == True:
        df_to_txt(property_summary,'stati_plot.txt')
    return property_summary
