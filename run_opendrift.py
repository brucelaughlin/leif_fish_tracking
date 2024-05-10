# Written by Bruce Laughlin (blaughli@ucsc.edu)



# This script is meant to be run from within the directory containing the excel (.xlsx) file 
# With TagID, lon, and lat.

# This script creates an output directory in the current directory (called "z_output"), in 
# which the tracking output netcdf files are stored.

# Once this runs successfully, run the next script ("modify_leif_csv.py") from the current directory.
# This will produce a new excel (.xlsx) file that contains 2 new columns, called "Initial Latitude" and "Initial Longitude"

# Finally, you can also create plots and movies for the tracking output

import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import os
import pandas as pd
from pathlib import Path
import sys

from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Input excel file name
#excel_file_in = "LocationDateForBruce.xlsx"
excel_file_in = sys.argv[1]
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Get the current directory, store in a variable
current_directory = os.getcwd()

# I typically create a directory called "z_output" in my project directory in which I store the Opendrift output
local_output_dir = 'z_output/'

# Combine the previous two strings variables to make a string specifying the directory for our Opendrfit output
output_dir = current_directory + '/' + local_output_dir

# Create the output directory if it doesn't exist yet
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Create a Pandas dataframe from the provided spreadsheet file
df = pd.read_excel(current_directory + "/" + excel_file_in)

# Create a list of run durations (each is 21 days, except for the last fish starting in baja, which is 300 days)
# NOTE:  This assumes that the model output data used by OpenDrift has a 1-day timestep.  For output with different
# temporal resolution, adjust accordingly (ie for 21 days, insteand of "21" below, use "21*24" if the output is hourly).
run_durations=[21] * (len(df.index) - 1)
run_durations.append(300)

# Define timesteps (in minutes) 
run_calc = 60
run_save = 60
#run_save = 1440
# convert timesteps to seconds
dt_calc = run_calc * 60
dt_save = run_save * 60;

# WE'RE RUNNING BACKWARDS, SO MAKE THE CALCULATION TIMESTEP NEGATIVE!!!!
dt_calc = -1*dt_calc

# Create a "base" datetime object that will be the reference time for everything, specified
# by the "zero time" of the model output hosted on the thredds server
thredds_datetime = datetime.datetime(1999,1,1,0,0)

# "object_type" must be specified for Leeway... don't think we'll need this with other models.  Computing this is 
# slightly involved, ask Bruce for more details if needed.
#object_type_number = 78 # This should correspond to the type of object specified in email correspondence

# Now we iterate through our dataframe, specifying seeding parameters for each particle and then running Opendrift.
# Note that there are multiple ways to handle the "seeding" of an Opendrift model.  Here, since I'm doing things 
# in a brute-force kind of way (ie creating a new model for each particle, rather than seeding all of the particles
# into a single model), I'm not making arrays/lists of seeding values, nor am I reading such values from
# an external file.  In my own research, I just make lists of lat/lon/depth/time values and then pass those
# all to the (seed.elements) method of the model object I create (see below).  That's not how they do things
# in the examples I've seen on the Opendrift web page (they either specify pre-defined "shapes" to seed, like cones,
# etc, or they load seed parameters from a file), but it was easy to implement and it's worked.  I can provide
# other scripts of mine for examples of how I handle seeding for larger experiments.

# This is a kind of weird iteration (ie two iterator variables rather than 1), which I'm not used to, but
# seems standard when working with Pandas dataframes
for idx, row in df.iterrows():

    # TEST: run once.  Comment out/remove the next two lines to run the full experiment.
#    if idx == 1:
#        break

    # read and assigne relevant parameters from the dataframe
    tagID = row['TagID']
    time_fish = row['Date To Start Backtracking']
    lat = row['Latitude']
    lon = row['Longitude']

    # In case "time_fish" is not a string, convert to string (maybe redundant)
    #time_fish = str(time_fish)
    time_fish_pre = str(time_fish)
    time_fish = datetime.datetime.strptime(time_fish_pre, '%Y-%m-%d %H:%M:%S')

    # Prepare name strings for the creation of output files
    tracking_output_pre = 'tracking_output_tag_ID_{}.nc'.format(tagID)
    #tracking_output_file = current_directory + '/' + local_output_dir + tracking_output_pre
    tracking_output_file = output_dir + tracking_output_pre

    # The UCSC thredds server url, which will be passed to the "reader" used by our model
    thredds_string = "https://oceanmodeling.ucsc.edu/thredds/dodsC/ccsra_2016a_phys_agg_zlevs/fmrc/CCSRA_2016a_Phys_ROMS_z-level_(depth)_Aggregation_best.ncd"
    
    # Instantiate the Opendrift model; here we're starting with "Leeway", as requested by Leif,
    # though we can try other ones as well (we have less than 10 particles and short drift times, so
    # we can try many models easily and compare output, for instance).

    # Note: "loglevel" is a parameter specifying how much text output Opendrift should generate while it's
    # running.  Setting it to 50 produces no printed output, setting it to 0 produces a bunch of output
    # (0 is the "debug"  mode, so that can be useful if errors are occurring).  I generally pipe this printed
    # output to a log file that I designate (ie Opendrift doesn't do this on its own), but for such a small
    # experiment I'm not worrying about saving logs at the moment.  More info/examples available upon request!

    #o = Leeway(loglevel = 20)
    o = OceanDrift(loglevel = 20)


    # Instantiate a "reader" to be used.  Should handle thredds urls.
    reader_thredds = reader_ROMS_native.Reader(thredds_string)
    # Add the reader to the model
    o.add_reader(reader_thredds)
   
    # In my own work, I specify that particles should "bounce" off of coasts rather than settle.  Seems like fish would bounce, right?
    o.set_config('general:coastline_action', 'previous')

    # Seed the particle
    #o.seed_elements(lon=lon, lat=lat, time=time_fish, object_type=object_type_number)
    #o.seed_elements(lon=lon, lat=lat, time=time_fish)
    o.seed_elements(lon=lon, lat=lat, time=time_fish, radius=1000, number=5000)

    o.run(outfile=tracking_output_file, duration=timedelta(days=run_durations[idx]), time_step=dt_calc, time_step_output=dt_save)






