import matplotlib.pyplot as plt
import numpy as np
import math
import stat_func

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
    plt.plot(x_t,stat_func.normal_dist(x_t,var_t,mu_t),label='normal_dist')
    plt.title(f'Thermostat damp={t_damp} ps')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.savefig('Thermostat.jpg',bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
    plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!
    
    plt.hist(df_p,bins=delta_p,density='True')
    plt.plot(x_p,stat_func.normal_dist(x_p,var_p,mu_p),label='normal_dist')
    plt.title(f'Barostat damp={p_damp} ps')
    plt.xlabel('Pressure (atm)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.savefig('Barostat.jpg',bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
    plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!


