# post_processing_tools

This repository host a series of python functions and libraries useful for the post processing of LAMMPS log.lammps file.
The content includes:
- library "filehandling" with in it libraries and functions for reading txt file, writing txt and xlsx files from dictionaries and parsing txt file.
- library "plotting" with functions for the creation of various plots of all the properties collected during the simulation.
- library "statis_calc" with function for the calculations of averages, std, plots of "key point" for the simulation based on averages, checks for thermostat and barostat and basic statistic functions.
- one dictionary for the units used in the simulation (units real of LAMMPS).
- one script that collect all the function mentioned above and is used for all the calculations at once (postprocessing.py).
- in progress...

Note: all this function are still in progress.
