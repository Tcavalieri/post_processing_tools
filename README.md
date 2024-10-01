# post_processing_tools

This repository host a series of python functions and modules useful for the post processing of LAMMPS log.lammps file.
The content includes:
- Module "filehandling" with in it libraries and functions for reading txt file, writing txt and xlsx files from dictionaries and parsing txt file
- Module "plotting" withn functions for the creation of various plots of all the properties collected during the simulation
- one function for computing the average of all the properties
- one function for checking the job of the barostat and thermostat used
- a library for generala statistic functions stat_func.py
- one dictionary for the units used in the simulation (units real of LAMMPS)
- one script that collect all the function mentioned above and is used for all the calculations at once (postprocessing.py).
- in progress...

Note: all this function are still in progress.
