import numpy as np
import math
import pandas as pd

from df_dict_to_txt import df_dict_to_txt
from df_dict_to_xlsx import df_dict_to_xlsx

# this function calculate the average, standard deviation and error of a given property data set
# dataframe: dataframe with all properties after a simulation (pandas dataframe if used data_parsing.py module)
# property: string that is the name of the property as it appear in the header of pandas_dataframe
# batch_factor: number of data in each batch for the calculations
# tol: tolerance for the comparison between batches

def stati(df_dict,units,batch_factor,tol):
    """
    the function calculate the average, standard deviation and tell the intervall of the average of all properties stored in all the tables stored in a dictionary.
    parameters:
    df_dict (dict): dictionary of pandas dataframe (=tables of data).
    units (dict): dictionary that stores the units of all properties (LAMMPS unit real)
    batch_factor (int): integer that tells how many batch you want and how many data in each one for the estimation of the intervall for the calculations. will be automatically modified if needed.
    tol (float): initial value for the tolerance criterion to establish the intervall for the calculations. if no convergence is reached it will be automaticaly updated.
    return:
    results (dict): dictionary with all the tables with all the calculations for each property. will be also stored in a file statistics.txt
    """
    results = {}
    
    for key in df_dict.keys():
        
        dataframe = df_dict[key]
        header = dataframe.columns
        t = dataframe[header[0]]/1000000
        n_batch = int(len(t)/batch_factor) # number of batches
        # check for compatibility of len(t) and batch_factor for the problem of len(t)<batch_factor or len(t)/batch_factor is not integer or too small
        if n_batch < 10:
            batch_factor = int(len(t)/10)
            n_batch = int(len(t)/batch_factor)
        # initialization for the collection of values
        calc_dict = {} # dictionary for all the properties values
        # the list of values for each key of the dict initialized 
        property = []
        unit_measure = []
        average = []
        dev_std = []
        delta_t = []
        tolerance = []

        for i in range(1,len(header)):
        
            sub_df = np.array(dataframe[header[i]]) # converting the column in a np array

            average_list = [] # initialization
            for n in range(0,n_batch):
                # slicing for the creation of a batch
                s_df = sub_df[(n)*batch_factor:(n+1)*batch_factor]
                m = np.mean(s_df)
                average_list.append(m)
            
            # this loop tell which batches are very similar and so they could be averaged together for better statystics
            k = 0
            err = 0 #counter that account for division by zero
            for ii in range(1,len(average_list)):
                # check for division by zero
                if average_list[ii-1] == 0:
                    err = err + 1
                    continue
                    
                if abs(1-abs((average_list[ii]/average_list[ii-1]))) < tol:
                    k = k + 1
            # printing for division by zero    
            if err >= 1:
                print('warning: division by zero encountered, maybe minim data')
                print(key + ' ' + header[i])
                print(f'division by zero encountered:{err}')
            # calculation of properties and storing in the dict
            property.append(header[i])
            unit_measure.append(units[header[i]])
            # this conditional handle the situation for which the block average has not satisfied the criterion tol
            if k == 0 and err == 0: # account also for the situation with zero values in minimization data
                factor = 10
                # this loop increase the tolerance criterion by a factor 10 at each iteration until convergence is reached
                esc = 0 # counter for escaping if convergence is not met in  max_step number of step
                flag = False
                while k == 0:
                    for ii in range(1,len(average_list)):
                        if abs(1-abs((average_list[ii]/average_list[ii-1]))) < tol*factor:
                            k = k + 1
                    factor = factor*10
                    # check for the number of step
                    if esc == 10:
                        print('max iterations reached: no convergence met, maybe minimization data')
                        print(key +' '+ header[i])
                        flag = True
                        break
                    else:
                        esc = esc + 1
                # handle the case of exceded the max number of iterations
                if flag == True:
                    average.append('none')
                    delta_t.append('none') 
                    dev_std.append('none') 
                    tolerance.append(tol*factor/10)  # /10 is to extract the right tolerance at the beginning of each step of the loop
                else:
                    ave = np.mean(sub_df[-k*batch_factor:])
                    average.append(ave)
                    tt = np.array(t[-k*batch_factor:])
                    delta_t.append(str(tt[0]) + '-' + str(tt[-1])) # extract the time intervall used for the average
                    var = np.sum((sub_df[-k*batch_factor:]-ave)**2)/len(sub_df[-k*batch_factor:]) # calculate variance
                    dev_std.append(math.sqrt(var)) # calculate standard deviation
                    tolerance.append(tol*factor/10)  # /10 is to extract the right tolerance at the beginning of each step of the loop
            else:
                if err > 1:
                    average.append('none')
                    delta_t.append('none') 
                    dev_std.append('none') 
                    tolerance.append('none') 
                else:  
                    ave = np.mean(sub_df[-k*batch_factor:])
                    average.append(ave)
                    tt = np.array(t[-k*batch_factor:])
                    delta_t.append(str(tt[0]) + '-' + str(tt[-1])) # extract the time intervall used for the average
                    var = np.sum((sub_df[-k*batch_factor:]-ave)**2)/len(sub_df[-k*batch_factor:]) # calculate variance
                    dev_std.append(math.sqrt(var)) # calculate standard deviation
                    tolerance.append(tol)
        # finalization of the dictionary with the calculated quantities
        calc_dict['Property'] = property
        calc_dict['Units'] = unit_measure
        calc_dict['Average'] = average
        calc_dict['Standard Deviation'] = dev_std
        calc_dict['Delta t (ns)'] = delta_t
        calc_dict['Tolerance'] = tolerance
        results[key + '_' +'properties'] = pd.DataFrame(calc_dict) # conversion of the dictionary in a pandas dataframe
    # creation of a txt file with the results
    df_dict_to_txt(results,'statistics.txt')
    df_dict_to_xlsx(results)

    return results
