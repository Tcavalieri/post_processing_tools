import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from filehandling import *
from units_dict import units
import math

def stati_plot(dict,txt_check,e_electro):
    '''
    Function that create a dictionary of dataframe with the property as columns and the mean and std for each table(step) in it (dataframe). It also plots the results.
    Parameters:
    dict (dict): a dictionary o dataframe with in it tables (step) as columns with in it all the relevant statistics for all the properties (dataframe).
    txt_check (boolean): if True it creates a txt file with all the results.
    e_electro (boolean): if True it creates a new entry for the total electrostatic energy.
    Return:
    property_summary (dict): dictionary of dataframes with all the values organised per property and inside per table.
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

# this function calculate the average, standard deviation and error of a given property data set
# dataframe: dataframe with all properties after a simulation (pandas dataframe if used data_parsing.py module)
# property: string that is the name of the property as it appear in the header of pandas_dataframe
# batch_factor: number of data in each batch for the calculations
# tol: tolerance for the comparison between batches

def stati(df_dict,units,n_batch,tol,max_iter,txt_check,xlsx_check,minim_check):
    """
    the function calculate the average, standard deviation and tell the intervall of the average of all properties stored in all the tables stored in a dictionary.
    parameters:
    df_dict (dict): dictionary of pandas dataframe (=tables of data).
    units (dict): dictionary that stores the units of all properties (LAMMPS unit real)
    batch_factor (int): integer that tells how many batch you want and how many data in each one for the estimation of the intervall for the calculations. will be automatically modified if needed.
    tol (float): initial value for the tolerance criterion to establish the intervall for the calculations. if no convergence is reached it will be automaticaly updated.
    txt_check (boolean): if True create a txt file with the results.
    xlsx_check (boolean): if True create multiple (as the number of tables) xlsx file with the results.
    minim_check (boolean): if True the minimization table is present and will be excluded in the calculations.
    max_iter (int): maximum number of iteration for the automatic update of the tolerance for convergence.
    return:
    results (dict): dictionary with all the tables with all the calculations for each property. will be also stored in a file statistics.txt
    """
    results = {}
    
    for key in df_dict.keys():
        
        if minim_check == True:
            # exclude minimization table
            if key == 'Table1':
                continue

        dataframe = df_dict[key]
        header = dataframe.columns
        t = dataframe[header[0]]/1000000
        nt = len(t)
        batch_points = int(len(t)/n_batch) # number of points in each batch

        # initialization for the collection of values
        calc_dict = {} # dictionary for all the properties values
        # the list of values for each key of the dict initialized 
        property = []
        unit_measure = []
        average = []
        dev_std = []
        delta_t = []
        tolerance = []
        n_points = []
        notes = []

        for i in range(1,len(header)):
        
            sub_df = np.array(dataframe[header[i]]) # converting the column in a np array

            average_list = [] # initialization
            for n in range(1,n_batch):
                # slicing for the creation of a batch
                if n == 1:
                    s_df = sub_df[(-n)*batch_points:]
                else:
                    s_df = sub_df[(nt-1)-(n)*batch_points:(nt-1)-(n-1)*batch_points]

                m = np.mean(s_df)
                average_list.append(m)
            
            # this loop tell which batches are very similar and so they could be averaged together for better statystics
            k = []
            err = 0 #counter that account for division by zero
            for ii in range(1,len(average_list)):
                # check for division by zero
                if average_list[ii-1] == 0:
                    err = err + 1
                    continue
                    
                if abs(1-abs((average_list[ii]/average_list[ii-1]))) < tol:
                    k.append(1)
                else:
                    k.append(0)
            
            # loop for checking that only the consecutive batches that satisfy the tolerance are considered and not all of them in random position in the dataset
            ref_k = 0
            for index in k:
                if index == 1:
                    ref_k = ref_k + 1
                else:
                    break   
            # printing for division by zero    
            if err >= 1:
                print('warning: division by zero encountered, maybe minim data')
                print(key + ' ' + header[i])
                print(f'division by zero encountered:{err}')
            # calculation of properties and storing in the dict
            property.append(header[i])
            unit_measure.append(units[header[i]])
            # this conditional handle the situation for which the block average has not satisfied the criterion tol
            if err > 1:
                average.append('none')
                delta_t.append('none') 
                dev_std.append('none') 
                tolerance.append('none')
                n_points.append('none')
                notes.append('WARNING') 
            elif ref_k == 0 and err == 0:  
                ave = np.mean(sub_df[-batch_points:])
                average.append(ave)
                tt = np.array(t[-batch_points:])
                delta_t.append(str(tt[0]) + '-' + str(tt[-1])) # extract the time intervall used for the average
                var = np.sum((sub_df[-batch_points:]-ave)**2)/len(sub_df[-batch_points:]) # calculate variance
                dev_std.append(math.sqrt(var)) # calculate standard deviation
                tolerance.append(tol)
                n_points.append(len(sub_df[-batch_points:]))
                notes.append('WARNING')
            else:
                ave = np.mean(sub_df[-(ref_k+1)*batch_points:])
                average.append(ave)
                tt = np.array(t[-(ref_k+1)*batch_points:])
                delta_t.append(str(tt[0]) + '-' + str(tt[-1])) # extract the time intervall used for the average
                var = np.sum((sub_df[-(ref_k+1)*batch_points:]-ave)**2)/len(sub_df[-(ref_k+1)*batch_points:]) # calculate variance
                dev_std.append(math.sqrt(var)) # calculate standard deviation
                tolerance.append(tol)
                n_points.append(len(sub_df[-(ref_k+1)*batch_points:]))
                notes.append('ok')
        # finalization of the dictionary with the calculated quantities
        calc_dict['Property'] = property
        calc_dict['Units'] = unit_measure
        calc_dict['Average'] = average
        calc_dict['Standard Deviation'] = dev_std
        calc_dict['Delta t (ns)'] = delta_t
        calc_dict['Tolerance'] = tolerance
        calc_dict['N points'] = n_points
        calc_dict['Notes'] = notes
        results[key + '_' +'properties'] = pd.DataFrame(calc_dict) # conversion of the dictionary in a pandas dataframe
    
    if txt_check == True:
        # creation of txt file with the results
        df_to_txt(results,'statistics.txt')
    if xlsx_check == True:
        # creation of xlsx files with the results
        df_to_xlsx(results)

    return results

def normal_dist(x,var,mu):
    """
    this function calculate the normal distribution probability density function
    parameters:
    x (np.array): intervall on x-axis for the calculations
    var (float): variance
    mu (float): average
    return:
    f (np.array): values of the normal distribution 
    """
    f = np.zeros(len(x))
    for i in range(len(x)):
        f[i] = 1/(math.sqrt(2*math.pi*var))*math.exp(-((x[i]-mu)**2)/(2*var))
    return f

def run_ave(properties,ignore_parm):
    """
    Function that calculate the running average exluding an initial set of point.
    Parameters:
    properties (list or np.array): raw data points.
    ignore_parm (float): float that tell to ignore an initial number of data from properties. range: 0-1  (recommended 0.2-0.4).
    Return:
    ra (list or np.array): the running average calculations
    """
    n = int(len(properties)*ignore_parm)
    properties_new = properties[n:]
    k = len(properties_new)
    ra = [0]*k
    ra[0] = properties_new[0]
    
    for i in range(1,k):
        ra[i] = (properties_new[i] + (i*ra[i-1]))/(i+1)
        
    return ra