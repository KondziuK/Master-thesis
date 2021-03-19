import sys
import os
import h5py

dir_general = os.path.join('\\v2e\\output\\')
dir_specyfic = 'tennis\\'
file = 'tennis.h5'
file_path = os.getcwd()+ dir_general + dir_specyfic +file

with h5py.File(file_path, "r") as f:
    # List all groups
    print(f"Keys: {f.keys()}")
    a_group_key = list(f.keys())[0]
    print(a_group_key)

    # Get the data
    data = list(f[a_group_key])[:10]
    print(data)



