import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statis_calc import run_ave, normal_dist
from units_dict import units
import math

def plots_maker(dict,units,ra_tol,x_tol,y_tol='none'):
    """
    Function that generate and store in files .jpg the plots of all the properties in all tables of data from a simulation with the running average.
    Parameters:
    dict (dict): dictionary with all the tables of data.
    units (dict): dictionary of units (LAMMPS unit real).
    ra_tol (float): float that tell to ignore an initial number of data in the running average calculation. range: 0-1  (recommended 0.2-0.4).
    x_tol (float): used to set the left limit of x axis as a percentage of the all duration. range: [0-1)
    y_tol (float): used to set the bottom and upper limit of y axis as a percentage of the last value of the running average. range: (0-1]. default 'none' use min and max as limits
    """
    # extract the different tables in the dictionary
    dict_keys = dict.keys()
    
    for key in dict_keys:
        # for each table extract the header
        dframe = dict[key]
        header = dframe.columns
        
        for k in range(len(header)):
            # the first header is the time so we extract it and skip to the thermodynamic properties
            if k == 0:
                t = np.array(dframe[header[k]])/1000000 # the /1000000 convert from fs to ns
                continue
            # creation of the file in which the plot will be stored
            file = key + '_' + header[k] + '.jpg'
            # calculation of the running average
            raw_data = np.array(dframe[header[k]])
            ra = run_ave(raw_data,ra_tol)
            
            # creation of the plot
            plt.plot(t,raw_data,label=header[k])
            plt.plot(t[len(t)-len(ra):],ra,label='Running_average')

            if y_tol == 'none':
                plt.ylim(min(raw_data[int(len(t)*x_tol):]),max(raw_data[int(len(t)*x_tol):]))
            else:
                plt.ylim(ra[-1]*(1-y_tol),ra[-1]*(1+y_tol))

            plt.xlim(t[int(-len(t)*x_tol)],t[-1])
            plt.xlabel('time (ns)')
            plt.ylabel(units[header[k]])
            plt.title(header[k])
            plt.grid(True)
            plt.legend()
            plt.savefig(file,bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
            plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!

def equilibration_plot(dict,minim_check,e_electro):
    '''
    function that produces plots of the all equilibration procedure for all the properties.
    Parameters:
    dict (dict): dictionary of dataframes with the data.
    minim_check (boolean): if True it exclude the minimization data.
    e_electro (boolean): if True create a plot for the total electrostatic energy.
    '''
    
    df = dict['Table2']
    for key in dict.keys():
        if minim_check == True:
            if key == 'Table1':
                continue
        if key == 'Table2':
            continue
        df = pd.concat([df,dict[key]],ignore_index=True)
    # conditional for evaluating the total electrostatic energy: E_coul+E_long    
    if e_electro == True:
        tt = np.array(df['Step'])/1000000
        e_long = np.array(df['E_long'])
        e_coul = np.array(df['E_coul'])
        e_long_coul = e_long + e_coul
        plt.plot(tt,e_long_coul)
        plt.xlabel('time (ns)')
        plt.ylabel('kcal/mol')
        plt.title('total electrostatic energy')
        plt.grid()
        plt.savefig('tot_electro_equil.jpg',bbox_inches='tight')
        plt.close('all')
        
    for name in df.columns:
        if name == 'Step':
            t = np.array(df[name])/1000000
            continue

        file = name + '_' + 'equil' + '.jpg'
        plt.plot(t,np.array(df[name]))
        plt.xlabel('time (ns)')
        plt.ylabel(units[name])
        plt.title(name)
        plt.grid(True)
        plt.savefig(file,bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
        plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!

def thermo_baros(data,table_name,t_damp,p_damp):
    """
    this function plots the probability density distribution as histograms for the temperature and pressure and compare it with normal distribution
    parameters:
    data (dict): dictionary of pandas dataframes with all the properties tables
    table_name (str): a string that tells which table to use
    t_damp (float): damping parameter for the thermostat
    p_damp (float): damping parameter for the barostat
    the output are two file .jpg for showing the plots
    """
    df = data[table_name] # choose the table you are interested in

    df_p = df['Press'] # extract pressure
    df_t = df['Temp'] # extract temperature

    # find the extremes values of the sets mentioned before
    min_p = math.ceil(min(df_p))
    max_p = math.ceil(max(df_p))

    min_t = math.ceil(min(df_t))
    max_t = math.ceil(max(df_t))

    delta_p = max_p-min_p
    delta_t = max_t-min_t

    # create array of values for normal distribution calculations  
    x_p = np.linspace(min_p,max_p,len(df_p))
    x_t = np.linspace(min_t,max_t,len(df_t))

    # adjust binning according to the differenze of extremes values
    if delta_p > 1000:
        delta_p = int(delta_p/6)
    if delta_t < 1000:
        delta_t = delta_t*2
    
    # calculate average and variance for both the datasets 
    mu_p = np.mean(np.array(df_p))
    var_p = np.sum((np.array(df_p)-mu_p)**2)/len(df_p)

    mu_t = np.mean(np.array(df_t))
    var_t = np.sum((np.array(df_t)-mu_t)**2)/len(df_t)

    # print the histograms and normal distributions for comparison
    # the value density = 'True' convert the frequency histogram to a probability density histogram
    plt.hist(df_t,bins=delta_t,density='True')
    plt.plot(x_t,normal_dist(x_t,var_t,mu_t),label='normal_dist')
    plt.title(f'Thermostat damp={t_damp} ps')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.savefig('Thermostat.jpg',bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
    plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!
    
    plt.hist(df_p,bins=delta_p,density='True')
    plt.plot(x_p,normal_dist(x_p,var_p,mu_p),label='normal_dist')
    plt.title(f'Barostat damp={p_damp} ps')
    plt.xlabel('Pressure (atm)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.savefig('Barostat.jpg',bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
    plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!


