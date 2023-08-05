#========================================================================#
# Script Name: GUI.py                                                    #
#                                                                        #
# Description: creates ConCorr GUIs                                  #
#                                                                        #
# Author:      Jen Burrell (March 8th, 2023)                             #
#========================================================================#

import PySimpleGUI as sg
import os
import filecmp
import logging
from misc import *
from datetime import datetime
# Add your new theme colors and settings
#sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#5B6858',
#                                        'TEXT': '#F6FFD5',
#                                        'INPUT': '#BA6D4A',
#                                        'TEXT_INPUT': '#000000',
#                                        'SCROLL': '#99CC99',
#                                        'BUTTON': ('#F6FFD5', '#424D5B'),
#                                        'PROGRESS': ('#D1826B', '#CC8019'),
#                                        'BORDER': 1, 'SLIDER_DEPTH': 0,
#                                        'PROGRESS_DEPTH': 0, }

sg.theme_global('GreenTan')   # Add a touch of color
### --- run starting GUI --- ###
def start_gui():
    info = {}
    center_column = [[sg.Text("Welcome to ConCorr")]]
    buttons = [
        [sg.Button('Load')],
        [sg.Button('Go'), sg.Button('Exit')]
        ]
    tab1_layout = [
        [sg.Text("Select your project working directory:"), sg.In(enable_events=True, key='-WDIR-'),sg.FolderBrowse('Select')],
        [sg.Text("Select a functional file that will be used in analysis:"), sg.Input(enable_events=True, key='-func_data-'), sg.FilesBrowse('Select')],
        [sg.Text("", enable_events=True, key='-oh_func-' ), sg.Button('Manual Selection', enable_events=True, visible=False, key='-oh_func_butt-')],
        [sg.VPush()],
        [sg.Text("Subjects found: "), sg.Text("None", enable_events=True, key='-sub_list-')],
        [sg.Text("Total # of Files found: "), sg.Text("None", enable_events=True, key='-file_list-')],
        [sg.Text("", enable_events=True, key='-move_on-')],
        ]
    tab2_layout = [
        [sg.Text("Select processing options below:")],
        [sg.Checkbox("Timeseries Generation", key='-timeseries-'), sg.Push(), sg.Button("info", key='-ts_butt-')],
        [sg.Text("Subject-Level processing:")],
        [sg.Checkbox("Correlation Matrix Generation", key='-sub_mat-'), sg.Push(), sg.Button("info", key='-sub_butt-')],
        [sg.Text("Group-Level processing:")],
        [sg.Checkbox("Correlation Matrix Generation", key='-grp_mat-'), sg.Push(), sg.Button("info", key='-grp_butt-')],
        [sg.Checkbox("Energy Landscape Analysis Toolbox Preprocessing", key='-ela_pre-'), sg.Push(), sg.Button("info", key='-ela_butt-')],
        [sg.Checkbox("Co-Activation Pattern Analysis Toolbox Preprocessing", key='-caps_pre-'), sg.Push(), sg.Button("info", key='-cap_butt-')],
        ]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [sg.TabGroup([[
            sg.Tab('DATA', tab1_layout, key= '-tab1-', tooltip='Where you specify your data'),
            sg.Tab('Processing', tab2_layout, key= '-tab2-', tooltip='Where you specify what happens to your data'),
            ]],enable_events=True)],
        [sg.VPush()],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('ConCorr', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Exit' or event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == '-WDIR-':
            WDIR = values['-WDIR-']
            try:
                sub_list = [i for i in os.listdir(f'{WDIR}/derivatives') if i.startswith("sub-")]
                sub_count = len(sub_list)
            except:
                sub_count = 0
            window['-sub_list-'].update(sub_count)
            info['WDIR'] = WDIR
            info['sub_count'] = sub_count
        elif event == '-func_data-':
            func_data = values['-func_data-']
            func_file = os.path.basename(func_data)
            file_names = [file for _, _, f in os.walk(f'{WDIR}/derivatives') for file in f if file.lower().endswith(func_file)]
            if len(file_names) < sub_count:
                window['-oh_func-'].update("Data could not be found please manually select data \nHint: your data has to be named the same across participants to be found automatically")
                window['-oh_func_butt-'].update(visible=True)
                window['Go'].update(disabled=True)
            file_count = len(file_names)
            window['-file_list-'].update(file_count)
            window['-move_on-'].update("If above information is correct, move on to Processing tab :)")
            info['func_data'] = values['-func_data-']
            info['file_names'] = file_names
        elif event == '-oh_func_butt-':
            by_hand_dict = by_hand()
            info['file_names'] = by_hand_dict['file_names']
            info['func_data'] = by_hand_dict['func_data']
            file_count = len(info['file_names'])
            window['-file_list-'].update(file_count)
            window['Go'].update(disabled=False)
        elif event == 'Load':
            load_info = load_gui()
            info = {**info, **load_info}
            WDIR = info['WDIR']
            try:
                sub_list = [i for i in os.listdir(f'{WDIR}/derivatives') if i.startswith("sub-")]
                sub_count = len(sub_list)
            except:
                sub_count = 'oops'
            file_count = len(info['file_names'])
            window['-sub_list-'].update(sub_count)
            window['-file_list-'].update(file_count)
            window['-move_on-'].update("If above information is correct, move on to Processing tab or 'Go' to use previous processing methods :)")
        elif event == '-ts_butt-':
            sg.popup_no_border("Timeseries Generation \n\nThis module will generate a timeseries based on the ROIs specified. \nYou are able to use your own ROI's by having a folder named 'ROIs' in your Project folder. \nYou can also choose from the available atlases included with ConCorr. \nAtlases include: Brainnetome, HCP-MMP1, HMAT, Juelich, and Schaefer \n\nMore information about atlases and Timeseries Generation can be found in the User Guide :)")
        elif event == '-sub_butt-':
            sg.popup_no_border("Subject-Level Correlation Matrix Generation \n\nThis module will generate correlation matrices for each functional file using timeseries from specified ROIs. Parameters such as correlation coeffiecient can be modified. \n\nMore information about Subject-Level Correlation Matrix Generation can be found in the User Guide :)")
        elif event == '-grp_butt-':
            sg.popup_no_border("Group-Level Correlation Matrix Generation \n\nThis module will generate averaged correlation matrices using timeseries from specified ROIs and a Design Matrix. Parameters such as correlation coeffiecient and group can be modified. \n\nMore information about Group-Level Correlation Matrix Generation can be found in the User Guide :)")
        elif event == '-ela_butt-':
            sg.popup_no_border("Energy Landscape Analysis Toolbox Preprocessing \n\nThis module will generate the necessary file types to run subject data through the Energy Landscape Analysis Toolbox (ELAT; Ezaki et al. PPhilosophical Transactions. Series A, Mathematical, Physical, and Engineering Sciences, 375(2096), 20160287 (2017)). \n\nMore information about Energy Landscape Analysis Toolbox Preprocessing can be found in the User Guide :)")
        elif event == '-cap_butt-':
            sg.popup_no_border("Co-Activation Pattern Analysis Toolbox Preprocessing \n\nThis module will generate the necessary file types to run subject data through the TbCAPs: A toolbox for co-activation pattern analysis (Bolton et al. NeuroImage, 211, 116621. (2020)). \n\nMore information about Energy Landscape Analysis Toolbox Preprocessing can be found in the User Guide :)")
        elif event == 'Go':
            info['Processing'] = [values['-timeseries-'], values['-sub_mat-'], values['-grp_mat-'], values['-ela_pre-'], values['-caps_pre-']]
            if not True in info['Processing']:
                info['Processing'] = load_info['Processing']
                if not True in info['Processing']:
                    sg.popup_no_border("No analysis has been choosen :(, \nif you want the program to do something go to the 'Processing' tab and select the analyses of your choice")
                    continue
            # - SAVE TEXT FILE OF INFO - #
            ConCorr_folder = f"{WDIR}/ConCorr/info"
            save_fld = mkdir(ConCorr_folder)
            file_list = [os.path.join(ConCorr_folder, f) for f in os.listdir(ConCorr_folder)]
            current = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            mkfile(f"{ConCorr_folder}/info_parts-{info['sub_count']}_files-{file_count}_{current}.txt", info)
            for file in file_list:
                samesies = filecmp.cmp(file, f"{ConCorr_folder}/info_parts-{info['sub_count']}_files-{file_count}_{current}.txt")
                if samesies:
                    os.remove(file)
            window.close()
    window.close()
    return info
    

def by_hand():
    ### --- Manual selection of Data --- ###
    info = {}
    all_files = []
    center_column = [[sg.Text("Manual Data Selection")]]
    file_list_column = [
        [sg.Text("Select a folder that contains data \nThen click all of the data files you want to include \nOnce all data appears in the list on the right, click 'Go'")],
        [sg.Text("Folder"), sg.In(size=(30, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
        [sg.Listbox(
            values=[],
            enable_events=True,
            size=(50, 20),
            key='-FILE_LIST-'
            )],
        ]
    file_viewer_column = [
        [sg.Text("Ensure all data files are in list before continuing", size=(50, 1))],
        [sg.Text("Files: ", size=(70, 3), key='-TOUT-')],
        [sg.Multiline(size=(70, 30), key='-TEXT-')]
        ]
    buttons = [[sg.Button('Go'), sg.Button('Exit')]]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [sg.Column(file_list_column), sg.VSeperator(), sg.Column(file_viewer_column)],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('ConCorr', layout, resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-FOLDER-':
            folder_location = values['-FOLDER-']
            try:
                files = os.listdir(folder_location)
            except:
                files = []
            file_names = [
                file for file in files
                if os.path.isfile(os.path.join(folder_location, file))
                and file.lower().endswith((".gz", ".nii"))
                ]
            window['-FILE_LIST-'].update(file_names)
        elif event == '-FILE_LIST-' and len(values['-FILE_LIST-']) > 0:
            if values['-FILE_LIST-'][0] not in all_files:
                all_files.append(values['-FILE_LIST-'][0])
            else:
                all_files.remove(values['-FILE_LIST-'][0])
            window['-TEXT-'].update(all_files)
        elif event == 'Go':
            info['file_names'] = all_files
#            func_data = os.path.join(folder_location, all_files[0]))
            info['func_data'] = os.path.join(folder_location, all_files[0])
            window.close()
    window.close()
    return info
    
def load_gui():
    ### --- Load info files --- ###
    info = {}
    center_column = [[sg.Text("Load info files")]]
    buttons = [[sg.Button('Load'), sg.Button('Cancel')]]
    content = [[sg.Text("Select info file to load: "), sg.In(size=(30, 1), enable_events=True, key='-load-'), sg.FileBrowse()]]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [content],
        [sg.VPush()],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('ConCorr', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == 'Load':
            load_file = values['-load-']
            if file_exists(load_file):
                info = load(load_file)
                info = info[0]
                window.close()
            else:
                sg.popup_no_border("Load file not found :( \nPlease try again or select data through data selection window")
    window.close()
    return info
            
        
def timeseries_gui():
    ### --- Present options for timeseries generation --- ###
    info = {}
    center_column = [[sg.Text("Timeseries Generation")]]
    buttons = [
        [sg.Button('Advanced')],
        [sg.Button('Go'), sg.Button('Exit')]
        ]
    content = [
        [sg.Text("How would you like to define your ROIs"), sg.Push(), sg.OptionMenu(['Brainnetome', 'HCP-MMP1', 'HMAT', 'Juelich', 'Schaefer', 'Provide your own ROIs'], default_value="...", key='-atlas-')],
        [sg.Text("Is your data in MNI space?"), sg.Push(), sg.OptionMenu(['Yes', 'No'], default_value="...", key='-data_space-')],
        [sg.Text("", enable_events=True, key='-out_text-' ), sg.Push(), sg.OptionMenu(['MNI space', 'Subject space'], default_value='MNI space', visible=False, key='-out_space-')]
        ]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [content],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    info['advanced'] = 'No'
    window = sg.Window('ConCorr', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Exit' or event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == 'Go':
            info['atlas'] = values['-atlas-']
            info['data_space'] = values['-data_space-']
            if '...' in info['atlas'] or '...' in info['atlas']:
                sg.popup_no_border("Selections required for processing")
                continue
            if info['data_space'] == 'No' and not 'out_space' in info:
                buttons_3 = [[sg.Button('Go'), sg.Button('Cancel')]]
                layout_3 = [
                    [sg.Text("Would you like to generate the timeseries in MNI space or in subject space?"), sg.Push(), sg.OptionMenu(['MNI space', 'Subject space'], default_value='...', key='-out_space-')],
                    [sg.VPush()],
                    [sg.VPush()],
                    [sg.Push(), sg.Column(buttons_3,element_justification='c'), sg.Push()],
                    ]
                window_3 = sg.Window("ConCorr",layout_3, resizable=True)
                while True:
                    event, values = window_3.read()
                    if event == 'Cancel' or event == sg.WIN_CLOSED:
                        break
                    if event == 'Go':
                        info['out_space'] = values['-out_space-']
                        window_3.close()
                window_3.close()
                continue
            else: info['out_space'] = 'MNI space'
            if info['atlas'] == 'Provide your own ROIs':
                info['atlas'] = 'Provided_ROIs'
                sg.popup_no_border("Provided ROIs must be in folder named 'ROIs' in your project working directory")
            if info['data_space'] == 'Yes' and info['out_space'] == 'Subject space':
                sg.popup_no_border("Data cannot be moved back into subject space, analysis will be done in MNI space")
                info['out_space'] = 'MNI space'
            window.close()
        elif event == 'Advanced':
            buttons_2 = [[sg.Button('Go'), sg.Button('Cancel')]]
            layout_2 = [
                [sg.Text("Set 'fslmaths' threshold for (0-1)"), sg.Input(enable_events=True, key='-thr-')],
                [sg.VPush()],
                [sg.VPush()],
                [sg.Push(), sg.Column(buttons_2,element_justification='c'), sg.Push()],
                ]
            window_2 = sg.Window("Advanced", layout_2, resizable=True)
            while True:
                event, values = window_2.read()
                if event == 'Cancel' or event == sg.WIN_CLOSED:
                    break
                if event == 'Go':
                    if not values['-thr-'] == '':
                        info['advanced'] = 'Yes'
                        info['thr'] = values['-thr-']
                    window_2.close()
            window_2.close()
    window.close()
    return info

def reg_gui():
    ### --- Throw error for registration -- ###
    info = {}
    text = "We weren't able to find the files necessary to normalize your data to MNI space,"
    text_2 = "you can normalize your subjects then try again, or choose to complete analysis in subject space"
    center_column = [
        [sg.Text("OH NO!")],
        [sg.Push()],
        [sg.Text(text)],
        [sg.Text(text_2)],
        [sg.Text(":(")],
        ]
    buttons = [[sg.Button("Fine I'll do it myself"), sg.Button("Subject Space!")]]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [sg.VPush()],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('ConCorr', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Exit' or event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == "Fine I'll do it myself":
            exit("User is going to do it themselves")
        elif event == "Subject Space!":
            info['out_space'] = "Subject space"
            window.close()
    window.close()
    return info

def sub_corr_gui():
    ### --- Present options for correlation matrix generation -- ###
    info = {}
    center_column = [[sg.Text("Subject-level Correlation Matrices")]]
    buttons = [[sg.Button('Go'), sg.Button('Exit')]]
    content = [
        [sg.Text("Select processing options below:")],[
        sg.Text("What atlas would you like to use?"), sg.Push(), sg.OptionMenu(['Brainnetome', 'HCP-MMP1', 'HMAT', 'Juelich', 'Schaefer', 'Provide your own ROIs'], default_value="...", key='-atlas-')],
        [sg.Text("Choose your correlation coefficent"), sg.Push(), sg.OptionMenu(['pearson', 'kendall', 'spearman'], default_value="pearson", key='-corr_coef-')],
        [sg.Text("Choose the method for testing and adjustment of pvalues"), sg.Push(), sg.OptionMenu(['none', 'bonf', 'sidak', 'holm', 'fdr_bh', 'fdr_by'], default_value='holm', key='-p_adjust-')],
        [sg.Text("Include Partial Correlations"), sg.Push(), sg.OptionMenu(['Yes', 'No'], default_value="Yes", key='-partial-')],
        [sg.Text("Include significance asterisk"), sg.Push(), sg.OptionMenu(['Yes', 'No'], default_value="Yes", key='-stars-')]
        ]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [sg.Push()],
        [content],
        [sg.VPush()],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('ConCorr', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Exit' or event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == 'Go':
            info['atlas'] = values['-atlas-']
            info['corr_coef'] = values['-corr_coef-']
            info['p_adjust'] = values['-p_adjust-']
            info['partial'] = values['-partial-']
            info['stars'] = values['-stars-']
            if info['atlas'] == 'Provide your own ROIs':
                info['atlas'] = 'Provided_ROIs'
            elif info['atlas'] == 'Schaefer':
                layout_2 = [
                    [sg.Text("Include a cluster matrix for Schaefer Networks?"), sg.Push(), sg.OptionMenu(['Yes', 'No'], default_value="Yes", key='-cluster-')],
                    [sg.Button("Ok"),sg.Button("Cancel")]]
                window_2 = sg.Window('Cluster Map?', layout_2, resizable=True, enable_close_attempted_event=True)
                while True:
                    event, values = window_2.read()
                    if event == sg.WIN_CLOSED:
                        break
                    if event == '-WINDOW CLOSE ATTEMPTED-':
                        exit("User exited ConCorr")
                    if event in 'Cancel':
                        info['cluster'] = 'No'
                        window_2.close()
                    if event == 'Ok':
                        info['cluster'] = values['-cluster-']
                        window_2.close()
                window_2.close()
            window.close()
    window.close()
    return info

def error_gui(error):
#        logging.error('Failed to do something: ' + str(e))
    ### --- Display Errors to user --- ###
    info = {}
    center_column = [[sg.Text("OH NO! \n  :(")]]
    buttons = [[sg.Button('Exit')]]
    content = [
        [sg.Text("The following error occurred:")],
        [sg.Text(error)],
        ]
    layout = [
        [sg.Push(), sg.Column(center_column,element_justification='c'), sg.Push()],
        [sg.Push()],
        [content],
        [sg.VPush()],
        [sg.Push(), sg.Column(buttons,element_justification='c'), sg.Push()],
        ]
    window = sg.Window('Error :(', layout, resizable=True, enable_close_attempted_event=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Exit' or event == '-WINDOW CLOSE ATTEMPTED-':
            exit("User exited ConCorr")
        elif event == 'Go':
            info['atlas'] = values['-atlas-']
            if info['atlas'] == 'Provide your own ROIs':
                info['atlas'] = 'Provided_ROIs'
            info['corr_coef'] = values['-corr_coef-']
            info['p_adjust'] = values['-p_adjust-']
            info['partial'] = values['-partial-']
            info['stars'] = values['-stars-']
            window.close()
    window.close()
    return info


