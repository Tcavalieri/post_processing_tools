# this function calculate the running average of a property. it needs a list as input with stored in it all the values of the property
# sampled at each time step. the length of the list is the total number of sampling of the property during the process. 
# knowing the time step and the total number of step is possibile to calculate the time of each sampling.
# the running average is a function of time but in simulations if the sampling of the properties is done at specific interval we cannot use
# the time to average the property, instead we use the index of the property value in the list given as input.
# this type of cumulative average is written recursively after giving the first point RA[0].
def running_average(properties,ignore_parm):
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