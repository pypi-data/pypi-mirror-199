#========================================================================#
# Script Name: mp_timeseries.py                                          #
#                                                                        #
# Description: This script defines functions that will allow users to    #
#              choose atlases to use to define ROIs and generate         #
#              timeseries                                                #
#                                                                        #
# Author:      Jen Burrell (March 21st, 2023)                            #
#========================================================================#
import os.path
import subprocess
import glob
import PySimpleGUI as sg
from misc import *
from itertools import repeat
import numpy as np
from multiprocessing import Pool

SDIR = os.path.dirname(__file__) # find where script is housed
#---------------------------------------#
#       Get data from chosen atlas      #
#---------------------------------------#
def get_atlas(atlas, WDIR, func):
    a = {'dir': (f"{SDIR}/Atlases/{atlas}")}
    pix_info = ''.join(str(subprocess.check_output(["fslinfo", f"{func}"])).split('\\t')).split('\\')
    pix_idx = [i for i, s in enumerate(pix_info) if 'npixdim1' in s]
    pix_dim = pix_info[pix_idx[0]].split("npixdim1")[1].split('.')[0]
    if atlas == "Brainnetome":
        a['lut'] = os.path.join(a['dir'], f"{atlas}.lut")
        a['file'] = os.path.join(a['dir'], f"BN_Atlas_246_{pix_dim}mm.nii.gz")
        a['file'] = os.path.basename(a['file'].strip())
        a['root'] = atlas
        min, a['max']  = subprocess.getoutput([f"fslstats {a['dir']}/{a['file']} -R"]).split()
    elif atlas == "Schaefer":
        layout = [
            [sg.Text("Select file for Schaefer parcellations:"), sg.Input(key='-File-', enable_events=True), sg.FilesBrowse('Select', key='-IN2-')],
            [sg.Button("Ok"),sg.Button("Cancel")]]
        window = sg.Window('Schaefer Parcellations', layout, resizable=True, enable_close_attempted_event=True)
        window["-IN2-"].InitialFolder = a['dir']
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == '-WINDOW CLOSE ATTEMPTED-':
                exit("User exited ConCorr")
            if event in 'Cancel':
                sg.popup_no_border("No file selected, please try again")
            if event == '-File-':
                a['file'] = values['-File-']
                window.close()
            if event == 'Ok':
                if 'file' in a and file_exists(a['file']):
                    window.close()
                else:
                    sg.popup_no_border("No file selected, please try again")
        window.close()
        a['file'] = a['file'].split('/')[-1]
        a['root'] = a['file'].split('_FSL')[0]
        a['lut'] = ''.join(glob.glob(os.path.join(a['dir'], "fsleyes_lut", f"{a['root']}*")))
        min, a['max']  = subprocess.getoutput([f"fslstats {a['dir']}/{a['file']} -R"]).split()
    elif atlas == "HCP-MMP1":
        a['lut'] = os.path.join(a['dir'], "HCP-MMP1_UniqueRegionList.txt")
        a['root'] = atlas
        a['file'] = "MMP_in_MNI_corr.nii.gz"
        min, a['max']  = subprocess.getoutput([f"fslstats {a['dir']}/{a['file']} -R"]).split()
    elif atlas == "Juelich":
        a['lut'] = os.path.join(a['dir'], "Juelich_atlas_index.txt")
        a['root'] = atlas
        a['file'] = "Juelich-maxprob-thr25-2mm.nii.gz"
        min, a['max']  = subprocess.getoutput([f"fslstats {a['dir']}/{a['file']} -R"]).split()
    elif atlas == "HMAT":
        a['lut'] = os.path.join(a['dir'], "HMAT_atlas_index.txt")
        a['root'] = atlas
        a['file'] = "HMAT.nii"
        min, a['max']  = subprocess.getoutput([f"fslstats {a['dir']}/{a['file']} -R"]).split()
    elif atlas == "Provided_ROIs":
        a['lut'] = ''
        a['root'] = atlas
        a['file'] = os.listdir(f"{WDIR}/ROIs")
        a['max'] = len(a['file'])
        a['dir'] = (f"{WDIR}/ROIs")
    else:
        raise ValueError(f"Unknown atlas {atlas}")
    return a
#---------------------------------------#
#           Mask Creation and           #
#         Timeseries generation         #
#---------------------------------------#
def run_timeseries(*dicts):
    user_info = {}
    for dict in dicts:
        user_info.update(dict)
    print(user_info)
    
    func_data = user_info['func_data']
    
    # - get path for all participants - #
    for char in func_data:
        if char.isdigit():
            func_data = func_data.replace(char, '*')
            
    dir_path_list = sorted(glob.glob(os.path.dirname(func_data))) # list of all files
    
    # - multiprocessing - #
    pool = Pool() # Create a multiprocessing Pool
    pool.starmap(get_masks, zip(dir_path_list, repeat(user_info))) # process gets masks
    pool.starmap(add_timeseries, zip(dir_path_list, repeat(user_info))) # process adds timeseries to master file
    # Close pool
    pool.close()
    pool.join()
    
#---------------------------------------#
#      Generate Masks & Timeseries      #
#---------------------------------------#
def get_masks(dir_path, user_info):
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
    
    func_file = os.path.basename(func_data)
    func_file_noext = func_file.split('.')[0] # file naming
        
    name_val = 1 # lut counting
    
    mkdir(dir_path,f"ROI_timeseries/{parce_name}")
    mkdir(dir_path,f"ROI_masks/{parce_name}")
            
    for value in range(1, int(float(max))+1):
        if atlas == "HCP-MMP1":
            atlas_lut_file = user_info['lut']
            name_val += 1  # accounts for space in data values
            roi_name = subprocess.check_output(f"sed -n '{name_val+1}p' {atlas_lut_file} | awk -F ',' '{{ print $1; }}'", shell=True).decode("utf-8").strip()  # get roi name from naming file
            if value >= 181:  # accounts for space in data values
                value += 20
        elif atlas == "Juelich":
            atlas_lut_file = user_info['lut']
            roi_name = subprocess.check_output(f"sed -n '{value+1}p' {atlas_lut_file} | awk -F '\\t' '{{ print $1; }}'", shell=True).decode("utf-8").strip()  # get roi name from naming file
            roi_name = roi_name.split(" ")[-1].replace(" ", "_")
        elif atlas == "Provided_ROIs":
            roi_name_file = os.listdir(atlas_directory)[value-1]
            roi_name = os.path.splitext(roi_name_file)[0]
            file_root = atlas
        elif atlas == "Schaefer":
            atlas_lut_file = user_info['lut']
            roi_name = subprocess.check_output(f"sed -n '{value}p' {atlas_lut_file} | awk '{{ print $5; }}'", shell=True).decode("utf-8").strip()  # get roi name from naming file
        else:
            atlas_lut_file = user_info['lut']
            roi_name = subprocess.check_output(f"sed -n '{value+1}p' {atlas_lut_file} | awk '{{ print $5; }}' | sed 's#/#_#g'", shell=True).decode("utf-8").strip()  # get roi name from naming file and remove any slashes
        ### --- output in MNI space --- ###
        if user_info['out_space'] == 'MNI space':
            if user_info['data_space'] == 'No': # check to see if data is in standard space
                ### --- Normalize subject data to MNI space --- ###
        ### - HAVE JUSTIN DOUBLE CHECK - ###
                if file_exists(f"{dir_path}/reg"):
                    subprocess.run(["flirt", "-ref", f"{dir_path}/reg/highres.nii.gz", "-in", f"{dir_path}/reg/example_func.nii.gz", "-dof", "6", "-omat", f"{dir_path}/reg/example_func2highres.mat"]) # produce affine matrix of registration of the example func to the highres file (struct)
                    subprocess.run(["flirt", "-ref", f"{FSLDIR}/data/standard/MNI152_T1_2mm_brain", "-in", f"{dir_path}/reg/highres.nii.gz", "-omat", f"{dir_path}/reg/highres2standard.mat"]) # produce affine matrix of registration of the highres file to standard space
                    subprocess.run(["convert_xfm", "-concat", f"{dir_path}/reg/example_func2highres.mat", f"{dir_path}/reg/highres2standard.mat", "-omat", f"{dir_path}/reg/example_func2standard.mat"]) # concatinates matrices to apply once
                    subprocess.run(["fnirt", f"--in={dir_path}/reg/highres_head.nii.gz", f"--aff={dir_path}/reg/highres2standard.mat", f"--cout={dir_path}/reg/highres2standard_warp.nii.gz", "--config=T1_2_MNI152_2mm"]) # produce the warp-field from registering the native space file to standard space, using parameters in T1_2_MNI152_2mm file
                    subprocess.run(["applywarp", "-i", f"{dir_path}/{func_file}", "-r", f"{dir_path}/reg/example_func.nii.gz", "-o", f"{dir_path}/{func_file_noext}_standard.nii.gz", f"--postmat={dir_path}/reg/example_func2standard.mat", f"--warp={dir_path}/reg/highres2standard_warp.nii.gz"]) # apply warp to func file such that it is in MNI space
                    func_file = f"{func_file_noext}_standard.nii.gz"
                else:
                    user_out = reg_gui()
                    user_info.update(user_out)
            ### --- generate masks --- ###
            if not file_exists(f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz"):
                if not file_exists(f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard"):
                    if atlas == "Provided_ROIs":
                        subprocess.run(["cp", f"{atlas_directory}/{roi_name_file}", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz"]) # copy user's masks to folder
                    else:
                        subprocess.run(["fslmaths", f"{atlas_directory}/{parce_file}", "-thr", f"{value}", "-uthr", f"{value}", "-bin", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz"]) # find ROI that matches value and remove everything else
                if file_exists(f"{dir_path}/reg/example_func2standard.nii.gz"):
                    subprocess.run(["flirt", "-in", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz", "-ref", f"{dir_path}/reg/example_func2standard.nii.gz", "-out", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz", "-usesqform", "-applyxfm"]) # aligns the NIFTI mm coordinates
                else:
                    subprocess.run(["flirt", "-in", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz", "-ref", f"{dir_path}/{func_file}", "-out", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz", "-usesqform", "-applyxfm"]) # aligns the NIFTI mm coordinates
                ###### THIS LINE MIGHT NOT BE USEFUL ####
                subprocess.run(["fslmaths", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz", "-thr", f"{user_thr}", "-bin", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz"]) # threshold and binarize MNI mask
                os.remove(f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz") # delete standard files
        ### --- output in subject space --- ###
        elif user_info['out_space'] == 'Subject space':
            if not file_exists(f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard.nii.gz"): # Check if ROI mask has been made
                subprocess.run(["fslmaths", f"{atlas_directory}/{parce_file}", "-thr", f"{value}", "-uthr", f"{value}", "-bin", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard"])
                if not file_exists(f"{dir_path}/reg/highres2standard_warp_inv.nii.gz"): # check if inverse warp exists, if not, run registrations and create it
                    subprocess.run(["flirt", "-ref", f"{dir_path}/reg/highres.nii.gz", "-in", f"{dir_path}/reg/example_func.nii.gz", "-dof", "6", "-omat", f"{dir_path}/reg/example_func2highres.mat"]) # produce affine matrix of registration of the example func to the highres file (struct)
                    subprocess.run(["flirt", "-ref", f"{FSLDIR}/data/standard/MNI152_T1_2mm_brain", "-in", f"{dir_path}/reg/highres.nii.gz", "-omat", f"{dir_path}/reg/highres2standard.mat"]) # produce affine matrix of registration of the highres file to standard space
                    subprocess.run(["fnirt", f"--in={dir_path}/reg/highres_head.nii.gz", f"--aff={dir_path}/reg/highres2standard.mat", f"--cout={dir_path}/reg/highres2standard_warp.nii.gz", "--config=T1_2_MNI152_2mm"]) # produce the warp-field from registering the native space file to standard space, using parameters in T1_2_MNI152_2mm file
                    subprocess.run(["convert_xfm", "-omat", f"{dir_path}/reg/highres2example_func.mat", "-inverse", f"{dir_path}/reg/example_func2highres.mat"]) # inverts transformation such that it registers highres to example_func
                    subprocess.run(["invwarp", f"--ref={dir_path}/reg/highres_head.nii.gz", f"--warp={dir_path}/reg/highres2standard_warp.nii.gz", f"--out={dir_path}/reg/highres2standard_warp_inv"]) # inverts the warp-field such that it registers standard to native space
                subprocess.run(["applywarp", "-i", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_standard", "-r", f"{dir_path}/reg/example_func.nii.gz", "-o", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func", f"--postmat={dir_path}/reg/highres2example_func.mat", "-w", f"{dir_path}/reg/highres2standard_warp_inv.nii.gz"]) # apply warp to ROI file such that it is in native functional space
                if not file_exists(f"{dir_path}/reg/example_func_brain_mask.nii.gz"):
                    subprocess.run(["bet", f"{dir_path}/reg/example_func.nii.gz", f"{dir_path}/reg/example_func_brain", "-f", "0.1", "-m"]) # create example functional brain mask via brain extraction
                subprocess.run(["fslmaths", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func", "-thr", f"{user_thr}", "-bin", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func"]) # threshold and binarize mask in native-space
                subprocess.run(["fslmaths", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func", "-mul", f"{dir_path}/reg/example_func_brain_mask", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func"]) # constrain mask to within the brain
        ### --- generate timeseries from masks--- ###
        if not file_exists(f"{dir_path}/ROI_timeseries/{parce_name}/{roi_name}_timeseries.txt"):
            get_timeseries(roi_name, f"{dir_path}/{func_file}", f"{dir_path}/ROI_timeseries/{parce_name}/{roi_name}_timeseries.txt", f"{dir_path}/ROI_masks/{parce_name}/{roi_name}_func.nii.gz")
            print(f"Extracting time series from {roi_name} ({value}/{max}) for {dir_path}")
 
 
#---------------------------------------#
#          Generate Timeseries          #
#---------------------------------------#
def get_timeseries(roi_name, input, out, mask, with_heading=True, print=True):
    if not file_exists(out):
        subprocess.run(["fslmeants", "-i", f"{input}", "-o", f"{out}", "-m", f"{mask}"])
    if with_heading == True:
        out_heading = ''.join([out.rsplit('.', 1)[0], '_w_heading.txt'])
        with open(out) as infile, open(out_heading, "w") as outfile:
            outfile.write(f"{roi_name}\n")
            outfile.write(infile.read())
            
#---------------------------------------#
#            Add Timeseries to          #
#             Master txt File           #
#---------------------------------------#
def add_timeseries(dir_path, user_info):
    parce_name = user_info['root'] # name of atlas
    input = sorted(glob.glob(f"{dir_path}/ROI_timeseries/{parce_name}/*_timeseries_w_heading.txt"))
    out =  f"{dir_path}/ROI_timeseries/{parce_name}_timeseries.txt"
    if not file_exists(out):
        file_dir = input[0].rsplit('/',1)[0]
        print(file_dir)
        columns =[]
        for file in input:
            with open(file, "r") as infile:
                new = np.array([line_num.rstrip() for line_num in infile.readlines()])
                columns.append(new)
        columns = np.vstack(columns).T
        np.savetxt(out, columns, fmt="%s", delimiter='\t')
    for file in input: os.remove(file)
        

if __name__ == '__main__':
    user_info = {'WDIR': '/Users/labmanager/Resilience', 'sub_count': 4, 'func_data': '/Users/labmanager/Resilience/derivatives/sub-01/ses-1/func/sub-01_ses-1_task-RS_run-1_bold.feat/filtered_func_data_denoised_standard.nii.gz', 'advanced': 'No', 'atlas': 'Brainnetome', 'data_space': 'Yes', 'out_space': 'MNI space', 'dir': '/Users/labmanager/JnJ_analyses/ConCorr/Atlases/Brainnetome', 'lut': '/Users/labmanager/JnJ_analyses/ConCorr/Atlases/Brainnetome/Brainnetome.lut', 'file': 'BN_Atlas_246_2mm.nii.gz', 'root': 'Brainnetome', 'max': '246.000000'}
    run_timeseries(user_info)
