from tools.filehandling import *
from tools.plotting import *
from tools.units_dict import units
from tools.statis_calc import *

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
table_name = 'Table33'
# batch factor for a sort of 'block average' (is not truly a block average!) in this case choosen to obtain 10 batch (10000 points collected)
batch = 1000
# tolerance for the calculation of the average values (empirically choosen and can be improved seing the results) (is also a guess because the program will automatically
# adjust it until convergence is met)
tol = 0.0005 # good guess especially for the density
# maximum number of iteration allowed
max_iter = 10


# calculations

# extract the data in the log file
Data = parsing('log.lammps',['Per','MPI','rank','memory'],['Loop','time','of'],txt_check=False,xlsx_check=False)

# create the plots of the properties
plots_maker(Data,units,ra_tol,xa_tol)

# analyze the behaviour of T and p
thermo_baros(Data,table_name,t_damp,p_damp)

# extract the average value of the properties
stati(Data,units,batch,tol,max_iter,txt_check=True,xlsx_check=False,minim_check=True)

# create equilibration plots
equilibration_plot(Data,minim_check=True)

