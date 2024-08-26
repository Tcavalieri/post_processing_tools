# post_processing_tools

This repository host a series of python functions useful for the post processing of LAMMPS log.lammps file.
The content includes:
- one functions able to read a .txt file
- a library dict_writing.py for writing dictionaries as .txt and .xlsx files
- one function for the parsing of the log.lammps output file
- one function for the creation of the plots of all the properties collected during the simulation
- one function for computing the average of all the properties
- one function for checking the job of the barostat and thermostat used
- a library for generala statistic functions stat_func.py
- one dictionary for the units used in the simulation (units real of LAMMPS)
- one script that collect all the function mentioned above and is used for all the calculations at once (postprocessing.py).

Note: all this function are still in progress.
