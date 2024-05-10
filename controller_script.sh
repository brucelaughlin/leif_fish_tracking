#!/bin/bash

# Written by Bruce Laughlin (blaughli@ucsc.edu)

# This bash script runs everything.

# Make this file executable (if it isn't already) by typing, in your bash terminal:
# chmod +x controller_script.sh

# Then, to run this script, type in your bash terminal:
# ./controller_script.sh



# ---------------------------------------------------
# ---------------------------------------------------
# Modify this to use a different excel file
# ---------------------------------------------------
csv_file="LocationDateForBruce.xlsx"
# ---------------------------------------------------
# ---------------------------------------------------


# Run Opendrift for all rows in the provided .xlxs sheet
python run_opendrift.py $csv_file






# ---------------------------------------------------
# Modifying CSV sheet and making plots is unecessary
# ---------------------------------------------------

## Create a modified .xlxs sheet with final (err, initial!) locations added as columns
#python modify_leif_csv.py

## Generate some simple plots and animations
#outputDir=$(pwd)/z_output
#fileArray=(${outputDir}/tracking_output_*.nc) 
#for file in ${fileArray[@]}
#do
#    python plot_animate_local.py $file
#done


