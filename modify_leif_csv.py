# Written by Bruce Laughlin (blaughli@ucsc.edu)

import os
import glob
import pandas as pd
import netCDF4
import numpy as np

# Input excel file name
excel_file_in = "LocationDateForBruce.xlsx"

# Output excel file name
excel_file_out = "LocationDataInitialFinal.xlsx"

# Store current directory name
current_directory = os.getcwd()

# Name of directory containing tracking output (relative to main project folder)
local_output_dir = '/z_output/'

# Full path to output directory
output_dir = current_directory + '/' + local_output_dir

# Create a Pandas dataframe from the provided spreadsheet file
df = pd.read_excel(current_directory + "/" + excel_file_in)

# Sort the dataframe by "TagID", since that's how our output files are ordered
# Note: Hopefully it's OK to return a CSV file ordered by TagID rather than the ordering initially provided
df.sort_values('TagID')

# Create lists which will hold the data to be added to the modified CSV file
num_rows = len(df.index)
lon_initial = []
lat_initial = []

# Create a list of the output files sorted by TagID
filename_list = []
for filename in glob.glob(output_dir  + "tracking_output_*.nc"):
    filename_list.append(filename)
filename_list.sort()

# Now append the final (ie initial) lat/lon from the runs to the lists we'll add to the CSV
for filename in filename_list:
    dset = netCDF4.Dataset(filename, 'r')
    lon_initial.append(list(np.array(dset['lon']).flatten())[-1]);
    lat_initial.append(list(np.array(dset['lat']).flatten())[-1]);
   

# Insert the "Initial Latitude" column as the 5th column
df.insert(4, "Initial Latitude", lat_initial)
# Insert the "Initial Longitude" column as the 6th column
df.insert(5, "Initial Longitude", lon_initial)

# Write the modified csv file
df.to_excel(excel_file_out)

