#======================================================================#
# Script Name: test_script.py                                          #
#                                                                      #
# Description: This script is used to test defined functions for bugs  #
#                                                                      #
# Author:      labmanager Burrell (March 10th, 2023)                          #
#======================================================================#
import os
import re
from timeseries import *
from GUI import *
from misc import *
from corr_mat import *
from datetime import datetime

### --- testing GUIs --- ###
#info = start_gui()
#print(info)

#info = timeseries_gui()
#print(info)
#exit()

### --- testing misc.py --- ###
info = sub_corr_gui()
print(info)
exit()

### --- testing timeseries.py --- ###
# - testing get_atlas - #
WDIR = "/Users/labmanager/Resilience"
atlas_input = "HCP-MMP1" ### TESTING
func = '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat/filtered_func_data_denoised_standard.nii.gz'
#
#atlas_info = get_atlas(atlas_input, WDIR, func)
#atlas = "HCP-MMP1"
##a = {'dir': (f"{SDIR}/Atlases/{atlas}"), 'file': 'Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'}
#a = {'dir': (f"{SDIR}/Atlases/{atlas}")}
#pix_info = ''.join(str(subprocess.check_output(["fslinfo", f"{func}"])).split('\\t')).split('\\')
#pix_idx = [i for i, s in enumerate(pix_info) if 'npixdim1' in s]
#pix_dim = pix_info[pix_idx[0]].split("npixdim1")[1].split('.')[0]
#a['lut'] = os.path.join(a['dir'], f"{atlas}.lut")
#a['file'] = os.path.join(a['dir'], f"BN_Atlas_246_{pix_dim}mm.nii.gz")
#a['root'] = a['file'].split('.')[0]
#print(a['root'].values)
#exit()

# - testing timeseries_run() - #
t_gui_info = {'atlas': 'Provided_ROIs', 'data_space': 'Yes', 'out_space': 'MNI space', 'advanced': 'No'}
atlas_info = {'dir': '/Users/labmanager/Resilience/ROIs', 'lut': [], 'root': 'Provided_ROIs', 'file': ['Hipp.nii', 'MPFC.nii', 'DMPFC.nii', 'PCC.nii', 'sgACC.nii', 'ACC.nii', 'VMPFC.nii', 'DLPFC.nii', 'RLPFC.nii'], 'max':9}
info = {'WDIR': '/Users/labmanager/Resilience', 'sub_count': 4, 'func_data': '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat/filtered_func_data_denoised_standard.nii.gz', 'file_names': ['filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz', 'filtered_func_data_denoised_standard.nii.gz'], 'Processing': [True, False, False, False, False]}
t_info = {x:info[x] for x in info if x in ('WDIR','sub_count','func_data')}
user_info = {'WDIR': '/Users/labmanager/Resilience', 'sub_count': 4, 'func_data': '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat/filtered_func_data_denoised_standard.nii.gz', 'advanced': 'No', 'atlas': 'Schaefer', 'data_space': 'Yes', 'out_space': 'MNI space', 'dir': '/Users/labmanager/JnJ_analyses/ConCorr/Atlases/Schaefer', 'file': 'Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz', 'root': 'Schaefer2018_100Parcels_7Networks_order', 'lut': '/Users/labmanager/JnJ_analyses/ConCorr/Atlases/Schaefer/fsleyes_lut/Schaefer2018_100Parcels_7Networks_order.lut', 'min': '0.000000', 'max': '100.000000'}
# - define variables in use - #
func_data = user_info['func_data']
atlas = user_info['atlas'] # name of atlas
atlas_lut_file = user_info['lut']
atlas_directory = user_info['dir']
parce_file = user_info['file'] # name of atlas file
parce_name = user_info['root'] # name of atlas
max = int(float(user_info['max']))
if user_info['advanced'] == 'Yes':
    user_thr = user_info['thr']
else:
    user_thr = 0.75

# - get path for all participants - #
for char in func_data:
    if char.isdigit():
        func_data = func_data.replace(char, '*')
        
dir_path_list = sorted(glob.glob(os.path.dirname(func_data))) # list of all files
file_list = {}
for i_sub in range(1, user_info['sub_count']+1):
    r = re.compile(f".*/sub-.{i_sub}/.*")
    files = list(filter(r.match, dir_path_list))
    file_list[f"{i_sub}"] = files
    
print(file_list['2'])
#run_timeseries(user_info)
exit()

# - Extras - #
#func_data = user_info['func_data']
#atlas = user_info['atlas'] # name of atlas
#atlas_lut_file = user_info['lut']
#atlas_directory = user_info['dir']
#parce_file = user_info['file'] # name of atlas file
#parce_name = user_info['root'] # name of atlas file
#roi_name = 'ACC'
#roi_name_file = 'ACC.nii'
#dir_path = '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat'
#func_file = 'filtered_func_data_denoised.nii.gz'

# - testing sub_corr_gui - #
#gui_info = sub_corr_gui()
c_gui_info = {'atlas': 'Provided_ROIs', 'corr_coef': 'Pearson', 'partial': 'Yes', 'stars': 'Yes'}
atlas_info = {'dir': '/Users/labmanager/Resilience/ROIs', 'lut': [], 'root': 'Provided_ROIs', 'file': ['Hipp.nii', 'MPFC.nii', 'DMPFC.nii', 'PCC.nii', 'sgACC.nii', 'ACC.nii', 'VMPFC.nii', 'DLPFC.nii', 'RLPFC.nii'], 'max':9}
c_info = {x:info[x] for x in info if x in ('WDIR','sub_count','func_data')}

#sub_corr(c_info, c_gui_info, atlas_info)
user_info = {'WDIR': '/Users/labmanager/Resilience', 'sub_count': 4, 'func_data': '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat/filtered_func_data_denoised_standard.nii.gz', 'atlas': 'Provided_ROIs', 'corr_coef': 'Pearson', 'partial': 'Yes', 'stars': 'Yes', 'dir': '/Users/labmanager/Resilience/ROIs', 'lut': [], 'root': 'Provided_ROIs', 'file': ['Hipp.nii', 'MPFC.nii', 'DMPFC.nii', 'PCC.nii', 'sgACC.nii', 'ACC.nii', 'VMPFC.nii', 'DLPFC.nii', 'RLPFC.nii'], 'max': 9}

parce_name = user_info['root'] # name of atlas
dir_path = '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat'
d1 = f"{dir_path}/ROI_timeseries/{parce_name}_timeseries.txt"
i_sub = list(filter(lambda x: "sub-" in x, d1.split("/")))[0].split('-')[1]

task_name = re.sub(f"bold.*/ROI_timeseries/{parce_name}_timeseries.txt", "", d1) # get rid of path after run specific information
task_name = task_name[task_name.find(i_sub):].split("/")[-1]

print(task_name)

