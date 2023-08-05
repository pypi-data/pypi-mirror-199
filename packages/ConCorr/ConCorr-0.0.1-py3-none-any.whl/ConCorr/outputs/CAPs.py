
### --- CAPS Analysis prep --- ###
if [[ "$caps_analysis" == "yes" ]] ; then
    ### --- Set up folders --- ###
    if [ ! -d "$dir_path/CAPs" ] ; then # check to see if ROI mask folder exists for this participant's run, if not make it
        mkdir -p $dir_path/CAPs
    fi
    if [ ! "$(ls -A $dir_path/CAPs)" ] ; then # checks to see if folder is empty, if it is then fill it with files
        fslsplit $dir_path/$func_data $dir_path/CAPs/vol_ -t # CAPs toolbox requires 3D files not 4D
        gunzip $dir_path/CAPs/* # and must be unziped
    fi
        fi
