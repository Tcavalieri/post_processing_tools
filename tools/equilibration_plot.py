import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from units_dict import units

def equilibration_plot(dict,minim_check,e_electro):
    '''
    function that produces plots of the all equilibration procedure for all the properties.
    Parameters:
    dict (dict): dictionary of dataframes with the data.
    minim_check (boolean): if True it exclude the minimization data.
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
