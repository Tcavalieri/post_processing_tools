# import the function for the parsing
from lammps_log_parsing import lammps_log_parsing
# import dictionary of units
from units_dict import units
# import the function for the creation of plots
from plots_maker import plots_maker
# import the post processing tools for the barostat and thermostat
from thermo_baros import thermo_baros
# import the properties calculator
from stati import stati

# input parameters for all the functions

# starting point as a percentage of the length of all data for the running average calculation (affects the plots)
ra_tol = 0.4
# starting point for showing the x-axis of the plots as a percentage of the all data length
xa_tol = 0.4
# extremes of y-axis as +/- as a percentage of the last value of running average for the plots maker function. the default is none and the function will adjust it based 
# on min max values
# y_tol = 
# damping parameter of the thermostat
t_damp = 10
# damping parameter of the barostat
p_damp = 10000
# name of the table you want to use for the barostat and thermostat. please remember that the minimization data table could create errors and crash. if is the 1st table,
# start from the 2nd
table_name = 'Table1'
# batch factor for a sort of 'block average' (is not truly a block average!) in this case choosen to obtain 10 batch (10000 points collected)
batch = 1000
# tolerance for the calculation of the average values (empirically choosen and can be improved seing the results) (is also a guess because the program will automatically
# adjust it until convergence is met)
tol = 0.0005 # good guess especially for the density


# calculations

# extract the data in the log file
Data = lammps_log_parsing('log.lammps')

# create the plots of the properties
plots_maker(Data,units,ra_tol,xa_tol)

# analyze the behaviour of T and p
thermo_baros(Data,table_name,t_damp,p_damp)

# extract the average value of the properties
stati(Data,units,batch,tol)



