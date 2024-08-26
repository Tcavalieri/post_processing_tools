import numpy as np
import math

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