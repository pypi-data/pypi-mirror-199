#========================================================================#
# Script Name: misc.py                                                   #
#                                                                        #
# Description: This script defines general functions that will to be     #
#              used by ConCorr                                       #
#                                                                        #
# Author:      Jen Burrell (March 10th, 2023)                            #
#========================================================================#
import os.path
import subprocess
import json
import shutil

# - make a directory - #
def mkdir(path,extension=''):
    path = os.path.join(path, extension)
    if not os.path.exists(path):
        os.makedirs(path)

# - check if file exists - #
def file_exists(filepath):
    return os.path.isfile(filepath)

# - make a file - #
def mkfile(name, content={}, *more):
    data = [content]
    for d in more:
        data.append(d)
    with open(name, 'w') as f:
        json.dump(data, f)
        
# - load file - #
def load(name):
    with open(name, "r") as f:
        info = json.load(f)
    return info

## - stop annoying warnings - #
#def fxn():
#    warnings.warn("deprecated", DeprecationWarning)

