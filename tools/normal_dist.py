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