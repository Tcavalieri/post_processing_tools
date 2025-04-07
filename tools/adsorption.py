import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import math




def adsorption(ext,mol,mass,normalisation_factor,ind_plot=False,count_norm=False):
    '''
    '''

    dat_files = []

    # iterating over all files
    for files in os.listdir():
        if files.endswith(ext):
            dat_files.append(files)  # printing file name of desired extension
        else:
            continue

    #dictionary of adsorption data
    ads_dict_raw = {}
    for file in dat_files:
        ads_dict_raw[file] = []

    for file in dat_files:
        with open(file,'r') as f:
            while True:
                readfile = f.readline()
                if not readfile:
                    break
                readfile = readfile.strip()
                readfile = readfile.split()
                ads_dict_raw[file].append(readfile)
        f.close()


    ads_dict = {}
    for key in ads_dict_raw.keys():
        raw_dat = ads_dict_raw[key]
        ads_dict[key] = pd.DataFrame(raw_dat[2:],columns=['t','N']).astype(float, errors='ignore')


    for key in ads_dict.keys():
        if ind_plot == False:
            continue
        df = ads_dict[key]
        plt.plot(np.array(df['t'])/1000000,np.array(df['N'])/2)
        plt.xlabel('time (ns)')
        plt.ylabel(f'{mol} molecules adsorbed')
        plt.title(f'{mol} adsorption in ZIF-8')
        plt.grid()
        plt.savefig(key+'.jpg',bbox_inches='tight')
        plt.close('all')

    ## isotherm point calculation ##

    isotherm = {}
    #p = [4, 6, 8, 10]
    #m_zif8 = mass #21847.27 # mass*Na

    aver_list = []
    var_list = []
    std_list = []
    p = []

    for key in ads_dict.keys():
        label_p = key.split('_')[1]
        df = ads_dict[key]
        if count_norm == False:
            Num = np.array(df['N'])
        else:
            Num = np.array(df['N'])/normalisation_factor
        aver = sum((Num[1999:]/mass))/len(Num[1999:])*1000
        var = np.sum(((Num[1999:]/mass*1000)-aver)**2)/len(Num[1999:])
        std = math.sqrt(var)

        aver_list.append(aver)
        var_list.append(var)
        std_list.append(std)
        p.append(float(label_p))

    isotherm[ext] = {
        'p': p,
        'average': aver_list,
        'variance': var_list,
        'standard_dev': std_list
    }
    #print(isotherm['N2'])

    isotherm_df = pd.DataFrame(isotherm[ext],columns=['p','average','variance','standard_dev'])
    isotherm_df = isotherm_df.sort_values(by='p')

    return isotherm_df

perez_exp_p = [
    
]

perez_exp_c = [
    
]

isotherm_co2 = adsorption('.CO2dat','CO2',21847.27,2,ind_plot=False,count_norm=False)
isotherm_n2 = adsorption('.N2dat','N2',21847.27,2,ind_plot=False,count_norm=True)
isotherm_ch4 = adsorption('.CH4dat','CH4',21847.27,2,ind_plot=False,count_norm=False)

#print(isotherm_df)
#plt.scatter(perez_exp_p,perez_exp_c, label='Perez P. et al 2010 [9]')
plt.errorbar(isotherm_co2['p'],isotherm_co2['average'],yerr=isotherm_co2['standard_dev'],color='g', label='CO2 PCFF + COMPASS')
plt.errorbar(isotherm_ch4['p'],isotherm_ch4['average'],yerr=isotherm_ch4['standard_dev'],color='b', label='CH4 PCFF + COMPASS')
plt.errorbar(isotherm_n2['p'],isotherm_n2['average'],yerr=isotherm_n2['standard_dev'],color='r', label='N2 PCFF + COMPASS')
plt.xlabel('pressure bar')
plt.ylabel('adsorption capacity mmol/g')
plt.title('Adsorption in ZIF-8 300 K')
plt.legend()
plt.grid()
plt.savefig('isotherms.jpg')
