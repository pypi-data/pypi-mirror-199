#==================================================================================#
# Script Name: ELA.py                                                              #
#                                                                                  #
# Description: lol who knows, nothing yet hopefully energy landscape analysis soon #
#                                                                                  #
# Authors:     Jen Burrell (Jan 30th, 2023)                                        #
#==================================================================================#
# To Do List:
# convert each roi timeseries to z-scores, (value - mean)/SD , where mean is the average activation level of the roi
# find average over time for each roi (empirical rate of activation)
# find averages of all pairwise products over time (empirical pairwise joint activation rate)
# fit a pairwise maximum entropy model (pMEM) * insert yoshi sound here *
#---------------------------------------#
#  Import relavent packages or install  #
#       if not done so already          #
#---------------------------------------#
import sys
import subprocess
import re
import itertools
import os
import warnings
import math
try:
    import numpy as np
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import numpy as np
try:
    import pandas as pd
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    import pandas as pd
try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib.pyplot'])
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
#---------------------------------------#
#             Get data from             #
#           Timecourse script           #
#---------------------------------------#
d1 = sys.argv[1] # data path
i_sub = sys.argv[2] # subject number
corr_out = sys.argv[3] # output path
atlas = sys.argv[4]
if sys.argv[5:]:
    atlas_lut = sys.argv[5]
task_name = re.sub(f"bold.*/ROI_timeseries/*_timeseries.txt", "", d1) # get rid of path after run specific information
task_name = task_name[task_name.find(i_sub):] # remove folders preceeding task information
task_name = task_name.split('bold', 1)[0] # only task specific information
corr_out = corr_out  + '/' # path includes subject folder
d1 = pd.read_csv(d1,sep='\t') # read in data
roi_list = list(d1.columns.values)  # get list of roi_names
if "Schaefer" in atlas: # get network names
    atlas_lut = pd.read_table(atlas_lut, sep=' ', header=None)
    net_names = atlas_lut.iloc[: , -1: ]
    net_names_raw = net_names.rename(columns={4:'Networks'})
    net_names = net_names[4].str.split('_', n=3, expand=True) # breaks string of network names
    net_names['Network'] = net_names[1] + "_" + net_names[2] # stitches together hemispheric networks
#    net_names['Network'] = net_names[2] # just networks
    net_comp = net_names[1] + "_" + net_names[2] + "_" + net_names[3]
    net_names = net_names.pop('Network') # gets network names
    d1.columns = net_names
    unq_names = pd.DataFrame(net_names.unique())

# - z-transformation - #
z_scaled = d1.copy()
for column in d1:
    z_scaled[column] = (z_scaled[column] - z_scaled[column].mean()) / z_scaled[column].std()
z_scaled = z_scaled.T
    
# - binarize - #
binary = pd.DataFrame(np.where(z_scaled>0, 1, 0), z_scaled.index, z_scaled.columns)

# - save dataframe to file - #
os.makedirs(corr_out + 'Stats/' + atlas + '/', exist_ok=True) # makes directory, or moves on
binary.to_csv(corr_out + 'Stats/' + atlas + '/' + task_name + 'binarized_timeseries.txt', index=None, header=None, sep=' ')

if "Schaefer" in atlas:
    # - average by network - #
    z_scaled_net = z_scaled.groupby(by=['Network']).mean()
   
    # - binarize - #
    binary = pd.DataFrame(np.where(z_scaled_net>0, 1, 0), z_scaled_net.index, z_scaled_net.columns)

    # - save dataframe to file - #
    os.makedirs(corr_out + 'Stats/' + atlas + '/', exist_ok=True) # makes directory, or moves on
    
    unq_names.to_csv(corr_out + 'Stats/' + atlas + '/timeseries_networks.dat', sep='\n', index=None, header=None, )
    binary.to_csv(corr_out + 'Stats/' + atlas + '/' + task_name + 'binarized_timeseries_net.txt', index=None, header=None, sep=' ')
