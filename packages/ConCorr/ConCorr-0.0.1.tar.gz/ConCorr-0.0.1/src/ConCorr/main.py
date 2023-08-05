#========================================================================#
# Script Name: main.py                                                   #
#                                                                        #
# Description: runs ConCorr GUI and calls processes chosen           #
#                                                                        #
# Author:      Jen Burrell (March 8th, 2023)                             #
#========================================================================#

import os
import logging
from GUI import *
from timeseries import *
from corr_mat import *

def main():
    info = start_gui()

    ### --- Call Requested Processing --- ###
    if info['Processing'][0] == True:
        # - Timeseries Processing - #
        t_info = {x:info[x] for x in info if x in ('WDIR','sub_count','func_data')}
        t_gui_info = timeseries_gui()
        atlas_info = get_atlas(t_gui_info['atlas'], info['WDIR'], info['func_data'])
        run_timeseries(t_info, t_gui_info, atlas_info)
    elif info['Processing'][1] == True:
        # - Sub-level Corr Matrix  - #
        c_info = {x:info[x] for x in info if x in ('WDIR','sub_count','func_data')}
        c_gui_info = sub_corr_gui()
        atlas_info = get_atlas(c_gui_info['atlas'], info['WDIR'], info['func_data'])
        corr_mat(c_info, c_gui_info, atlas_info)
    #elif info['Processing'][2] == True:
    #    # - Grp-level Corr Matrix - #
    #    grp_corr()
    #elif info['Processing'][3] == True:
    #    # - ELA Processing - #
    #    ela()
    #elif info['Processing'][4] == True:
    #    # - CAPs Processing - #
    #    caps()

if __name__ == '__main__':
#    try:
    main()
#    except BaseException as e:
#        error_gui(e)
### ERROR NOT WORKING RIGHT
