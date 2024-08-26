import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import stat_func

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
            ra = stat_func.run_ave(raw_data,ra_tol)
            
            # creation of the plot
            plt.plot(t,raw_data,label=header[k])
            plt.plot(t[len(t)-len(ra):],ra,label='Running_average')

            if y_tol == 'none':
                plt.ylim(min(raw_data[int(len(t)*x_tol):]),max(raw_data[int(len(t)*x_tol):]))
            else:
                plt.ylim(ra[-1]*(1-y_tol),ra[-1]*(1+y_tol))

            plt.xlim(t[-1]*x_tol,t[-1])
            plt.xlabel('time (ns)')
            plt.ylabel(units[header[k]])
            plt.title(header[k])
            plt.grid(True)
            plt.legend()
            plt.savefig(file,bbox_inches='tight') # remember to save the plot in the file created before (bbox.. to solve ylabel cut out)(to increase dimensionof figure use dpi=(integer))
            plt.close('all') # very important to close the file once finished, otherwise at each step we obtain a cumulative plot !!

