#========================================================================#
# Script Name: correlation_group.py                                      #
#                                                                        #
# Description: Script creates allows for the creation of different correlation     #
#              matrices with full and partial correlations from different group    #
#              connections from time courses generate by parent script   #
#              'Timecourse_JandJ.sh'                                     #
#                                                                        #
# Authors:      Jen Burrell (Dec 7th, 2022)                              #
#========================================================================#
# To Do List:

#---------------------------------------#
#  Import relavent packages or install  #
#       if not done so already          #
#---------------------------------------#
import sys
import subprocess
import re
import itertools
import os
import glob
import warnings
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
    import seaborn as sns
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'seaborn'])
    import seaborn as sns
try:
    import matplotlib.pyplot as plt
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib.pyplot'])
    import matplotlib.pyplot as plt
try:
    import pingouin as pg
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pingouin'])
    import pingouin as pg

#---------------------------------------#
#         Get directories from          #
#           Timecourse script           #
#---------------------------------------#
derivatives = sys.argv[1] # derivatives path
corr_out = sys.argv[2] + '/' # output path
sub_list = sys.argv[3] # subject list
sub_list = sorted(sub_list.split(','))
ses_list = sys.argv[4] # session list
ses_list = sorted(ses_list.split(','))
atlas = sys.argv[5]
design = corr_out + 'design_matrix.csv'
d_mat = pd.read_csv(design, header=None) # read in design matrix

### --- Set up Stats readout --- ###
# - ONLY WORKS WITH SQUARE DATA - #
d_mat = d_mat.fillna(0)
d_list = d_mat.values.tolist()
d_list_flat = d_mat.values.flatten().tolist()
sub_list_ex = []
ses_list_ex = []
run_list = []
col_list = []
if len(ses_list)>0:
    for i_part in range(len(d_list)):
        for i_run in range(len(d_list_flat)//len(d_list)):
            run_list.append('run-' + str(i_run+1))
            sub_list_ex.append(sub_list[i_part])
            for ses_num in range(len(ses_list)):
                for i_ses in range((len(d_list_flat)//len(d_list))//len(ses_list)):
                    ses_list_ex.append(ses_list[ses_num])
    small_list = list(zip(d_list_flat, sub_list_ex, ses_list_ex, run_list))
    col_list.append(['Group','Subject','Session','Run'])
else:
    for i_part in range(len(d_list)):
        for i_run in range(len(d_list_flat)//len(d_list)):
            run_list.append('run-' + str(i_run+1))
            sub_list_ex.append(sub_list[i_part])
    small_list = list(zip(d_list_flat, sub_list_ex, run_list))
    col_list.append(['Group','Subject','Run'])

#---------------------------------------#
#          Find data from files         #
#---------------------------------------#
stats_files = []
part_files = []
full_files = []
full_r_data = []
full_z_data = []
part_r_data = []
part_z_data = []
for i_sub in sub_list:
    stats_path = corr_out + i_sub + '/Stats/' + atlas
    for result in glob.iglob(stats_path):
        for root, dirs, files in os.walk(result, topdown=False):
            for name in files:
                if name.endswith("corr_stats.csv"):
                    stats_files.append(os.path.join(root, name)) # get all files with path
stats_files.sort() # sort so runs and participants are in the right order
full_files = list(filter(lambda substring: "full" in substring, stats_files))
part_files = list(filter(lambda substring: "partial" in substring, stats_files))

### --- Set up Stats readout --- ###
# - ONLY WORKS WITH SQUARE DATA - #
f_data_list =[]
med_list = []
for file in full_files:
    full_data = pd.read_csv(file, sep=',') # read in data
    roi_names = full_data.loc[:,"X"] # both lists are incomplete
    roi_names_2 = full_data.loc[:,"Y"]
    roi_pairs = [(roi_names[i], roi_names_2[i]) for i in range(0, len(roi_names))]
    roi_pairs = ['-'.join(sub_list) for sub_list in roi_pairs]
    full_z_data = full_data.loc[:,"Fishers Z"].values
    full_r_data = full_data.loc[:,"r"].values
    f_data_list.append(list(zip(roi_pairs,full_r_data,full_z_data)))
flat_list = [item for sublist in f_data_list for item in sublist]
col_list.append(['Roi_Pairs','Pearsons_R',"Fishers_Z"])
col_list = [item for sublist in col_list for item in sublist]
for i_data in range(len(small_list)):
    for i_roi in range(len(roi_pairs)):
        med_list.append(small_list[i_data])
big_list = list(zip(med_list,flat_list))
big_flat_list = [item for sublist in big_list for item in sublist]
really_flat_list = [item for sublist in big_flat_list for item in sublist]
less_flat_list = list(itertools.zip_longest(*[iter(really_flat_list)]*len(col_list)))
if len(ses_list)>0:
    f_stats = pd.DataFrame(less_flat_list, columns=col_list)
else:
    f_stats = pd.DataFrame(less_flat_list, columns=col_list)
os.makedirs(corr_out + 'Stats/' + atlas + '/', exist_ok=True) # makes directory, or moves on
f_stats.to_csv(corr_out  + 'Stats/' + atlas + '/Full_group_stats_{atlas}.csv', compression=None, index=False) # save partial correlation stats table

#---------------------------------------#
#             Design Matrix             #
#---------------------------------------#
pos_list = [(d_mat[d_mat[col].eq(1)].index[i], d_mat.columns.get_loc(col)) for col in d_mat.columns for i in range(len(d_mat[d_mat[col].eq(1)].index))]
neg_list = [(d_mat[d_mat[col].eq(-1)].index[i], d_mat.columns.get_loc(col)) for col in d_mat.columns for i in range(len(d_mat[d_mat[col].eq(-1)].index))]
pos_df = pd.DataFrame(pos_list, columns =['Part', 'Run'])
neg_df = pd.DataFrame(neg_list, columns =['Part', 'Run'])

f_files_dic = {}
p_files_dic = {}
f_pos_files = []
p_pos_files = []
f_neg_files = []
p_neg_files = []
for i_part in sub_list:
    f_files_dic[i_part] = list(filter(lambda x: i_part in x, full_files))
    f_files_df = pd.DataFrame.from_dict(f_files_dic, orient='index')
    p_files_dic[i_part] = list(filter(lambda x: i_part in x, part_files))
    p_files_df = pd.DataFrame.from_dict(p_files_dic, orient='index')

if len(part_files)>0:
    for i in range(len(pos_df)):
        f_pos_files.append(f_files_df.iloc[pos_list[i]])
        p_pos_files.append(p_files_df.iloc[pos_list[i]])
    for i in range(len(neg_df)):
        f_neg_files.append(f_files_df.iloc[neg_list[i]])
        p_neg_files.append(p_files_df.iloc[neg_list[i]])
else:
    for i in range(len(pos_df)):
        f_pos_files.append(f_files_df.iloc[pos_list[i]])
    for i in range(len(neg_df)):
        f_neg_files.append(f_files_df.iloc[neg_list[i]])

task_list = []
z_data = []
### --- full data from files --- ###
# - positive data - #
task_list = []
z_data = []
for file in f_pos_files:
    task_name = re.sub("_full_corr_stats.csv", "", file) # get rid of path after run specific information
    task_name = task_name.split("/")[-1] # only run specific information
    task_list.append(task_name) # all of the tasks
    full_data = pd.read_csv(file, sep=',') # read in data
    roi_names = full_data.loc[:,"X"] # both lists are incomplete
    roi_names_2 = full_data.loc[:,"Y"]
    z_data.append(full_data.loc[:,"Fishers Z"].values)

f_pos_z_data = {}
z_data = np.array(z_data) # array of arrays holding all of the z data from files
f_pos_z_data = pd.DataFrame(data=z_data.T, columns=[task_list]) # turns array into dataframe with columns for each file

# - negative data - #
if len(neg_list)>0:
    task_list = []
    z_data = []
    for file in f_neg_files:
        task_name = re.sub("_full_corr_stats.csv", "", file) # get rid of path after run specific information
        task_name = task_name.split("/")[-1] # only run specific information
        task_list.append(task_name) # all of the tasks
        full_data = pd.read_csv(file, sep=',') # read in data
        roi_names = full_data.loc[:,"X"] # both lists are incomplete
        roi_names_2 = full_data.loc[:,"Y"]
        z_data.append(full_data.loc[:,"Fishers Z"].values)

    f_neg_z_data = {}
    z_data = np.array(z_data) # array of arrays holding all of the z data from files
    f_neg_z_data = pd.DataFrame(data=z_data.T, columns=[task_list]) # turns array into dataframe with columns for each file

### --- partial data from files --- ###
if len(part_files)>0:
    # - positive data - #
    task_list = []
    z_data = []
    for file in p_pos_files:
        task_name = re.sub("_partial_corr_stats.csv", "", file) # get rid of path after run specific information
        task_name = task_name.split("/")[-1] # only run specific information
        task_list.append(task_name) # all of the tasks
        part_data = pd.read_csv(file, sep=',') # read in data
        z_data.append(part_data.loc[:,"Fishers Z"].values)
        
    p_pos_z_data = {}
    z_data = np.array(z_data) # array of arrays holding all of the z data from files
    p_pos_z_data = pd.DataFrame(data=z_data.T, columns=[task_list]) # turns array into dataframe with columns for each file
    
    # - negative data - #
    if len(neg_list)>0:
        task_list = []
        z_data = []
        for file in p_neg_files:
            task_name = re.sub("_partial_corr_stats.csv", "", file) # get rid of path after run specific information
            task_name = task_name.split("/")[-1] # only run specific information
            task_list.append(task_name) # all of the tasks
            part_data = pd.read_csv(file, sep=',') # read in data
            z_data.append(part_data.loc[:,"Fishers Z"].values)
        
        p_neg_z_data = {}
        z_data = np.array(z_data) # array of arrays holding all of the z data from files
        if len(z_data)>0:
            p_neg_z_data = pd.DataFrame(data=z_data.T, columns=[task_list]) # turns array into dataframe with columns for each file
    
    ### --- calculate data --- ###
    f_pos_avg = f_pos_z_data.mean(axis=1)
    p_pos_avg = p_pos_z_data.mean(axis=1)
    if len(neg_list)>0:
        f_neg_avg = f_neg_z_data.mean(axis=1)
        p_neg_avg = p_neg_z_data.mean(axis=1)
    
        pos_neg_full = f_pos_avg - f_neg_avg
        pos_neg_part = p_pos_avg - p_neg_avg
    else:
        pos_neg_full = f_pos_avg
        pos_neg_part = p_pos_avg
        
    roi_names = pd.concat([roi_names, roi_names_2]) # concatenate lists
    roi_names = list(dict.fromkeys(roi_names)) # make the names into dictionary key terms then create list, there by removing doubles of any entry
    
    ### --- full matrix --- ###
    group_mat_full = np.zeros((len(roi_names),len(roi_names)))
    triu = np.triu_indices(len(roi_names), k = 1)
    tril = np.tril_indices(len(roi_names), -1)
    index = np.triu_indices_from(group_mat_full, k = 1)
    group_mat_full[triu] = pos_neg_full[:]
    group_mat_full[tril] = group_mat_full.T[tril]

    ### --- partial matrix --- ###
    group_mat_part = np.zeros((len(roi_names),len(roi_names)))
    triu = np.triu_indices(len(roi_names), k = 1)
    tril = np.tril_indices(len(roi_names), -1)
    index = np.triu_indices_from(group_mat_part, k = 1)
    group_mat_part[triu] = pos_neg_part[:]
    group_mat_part[tril] = group_mat_part.T[tril]
else:
    ### --- calculate data --- ###
    f_pos_avg = f_pos_z_data.mean(axis=1)
    if len(neg_list)>0:
        f_neg_avg = f_neg_z_data.mean(axis=1)
        
        pos_neg_full = f_pos_avg - f_neg_avg
    else:
        pos_neg_full = f_pos_avg
    
    roi_names = pd.concat([roi_names, roi_names_2]) # concatenate lists
    roi_names = list(dict.fromkeys(roi_names)) # make the names into dictionary key terms then create list, there by removing doubles of any entry
    
    ### --- full matrix --- ###
    group_mat_full = np.zeros((len(roi_names),len(roi_names)))
    triu = np.triu_indices(len(roi_names), k = 1)
    tril = np.tril_indices(len(roi_names), -1)
    index = np.triu_indices_from(group_mat_full, k = 1)
    group_mat_full[triu] = pos_neg_full[:]
    group_mat_full[tril] = group_mat_full.T[tril]
    
### --- masks --- ###
mask1 = np.triu(np.ones_like(group_mat_full, dtype=bool)) # mask for upper triangle (data appears in lower triangle)
mask2 = np.tril(np.ones_like(group_mat_full, dtype=bool)) # mask for lower triangle (data appears in upper triangle)

### --- Figure Generation --- ###
if len(part_files)>0:
    if len(group_mat_full) <= 30:
        sns.set_theme(style="white")
        fig, ax = plt.subplots(figsize=(11, 9))
        ax.set(title=f"Group mean Fisher's z-scores subtraction matrix")

        sns.heatmap(group_mat_full, mask=mask1, cmap='Blues', square=True, linewidths=.0, xticklabels = roi_names, yticklabels = roi_names, cbar_kws={"shrink": .66, "pad":.02, 'label': 'Full Correlations'}) # full correlation in lower triangle
        sns.heatmap(group_mat_part, mask=mask2, cmap='YlOrBr',square=True, linewidths=.0, xticklabels = roi_names, yticklabels = roi_names, cbar_kws={"shrink": .66, 'label': 'Partial Correlations'}) # partial correlation in upper triangle
        ax.patch.set_facecolor('black') # diagonals

#        plt.show() # uncomment to see image at generation
        os.makedirs(corr_out + 'Group_Images/', exist_ok=True) # makes directory, or moves on
        plt.savefig(corr_out + 'Group_Images/' f'avg-corr-mat_subtract_{atlas}.png') # saves image folder of subject folder in
    else:
        sns.set_theme(style="white")
        labels = [*range(0, len(group_mat_full)+1, (len(group_mat_full))//10)]
        fig, ax = plt.subplots(figsize=(11, 9))
        ax.set(title=f"Group mean Fisher's z-scores subtraction matrix")

        sns.heatmap(group_mat_full, mask=mask1, cmap='Blues', square=True, linewidths=.0, xticklabels=labels, yticklabels=labels, cbar_kws={"shrink": .66, "pad":.02, 'label': 'Full Correlations'}) # full correlation in lower triangle
        sns.heatmap(group_mat_part, mask=mask2, cmap='YlOrBr',square=True, linewidths=.0, xticklabels=labels, yticklabels=labels, cbar_kws={"shrink": .66, 'label': 'Partial Correlations'}) # partial correlation in upper triangle
        ax.patch.set_facecolor('black') # diagonals
        ax.set_xticks(labels, labels=labels)
        ax.set_yticks(labels, labels=labels)

#        plt.show() # uncomment to see image at generation
        os.makedirs(corr_out + 'Group_Images/', exist_ok=True) # makes directory, or moves on
        plt.savefig(corr_out + 'Group_Images/' f'avg-corr-mat_subtract_{atlas}.png') # saves image folder of subject folder in
else:
    sns.set_theme(style="white")
    labels = [*range(0, len(group_mat_full)+1, (len(group_mat_full))//10)]
    fig, ax = plt.subplots(figsize=(11, 9))
    
    sns.heatmap(group_mat_full, cmap="viridis", square=True, rasterized=True, xticklabels=labels, yticklabels=labels, cbar_kws={"shrink": .66, "pad":.02, 'label': 'Full Correlations'}) # full correlation in lower triangle
    ax.patch.set_facecolor('black') # diagonals
    ax.set(title="Group mean Fisher's z-scores subtraction matrix", xlabel='Nodes', ylabel='Nodes')
    ax.set_xticks(labels, labels=labels)
    ax.set_yticks(labels, labels=labels)
    
#    plt.show() # uncomment to see image at generation
    os.makedirs(corr_out + 'Group_Images/', exist_ok=True) # makes directory, or moves on
    plt.savefig(corr_out + 'Group_Images/' f'avg-corr-mat_subtract_{atlas}.png') # saves image folder of subject folder in
