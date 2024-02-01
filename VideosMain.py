# James Caldwell
# University of Virginia, Center for Applied Biomechanics
# January 2024

# This code is use for tracking the status of video files
    # Each run has 3 camera angles, which output a raw .MCF file. 
    # Each .MCF needs to be converted to .AVI
    # Each .AVI needs to be compressed
    # Written because 2024 Turf testing created ~4000 video files
# Inputs: This script takes in a run log, Video Log.xlsx, "\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video\Video Log.xlsx"
# Outputs: The script creates 2 excel files: 
    # Video Log Highlighted.xlsx: The same as the original video log, modified for all files that exist highlighted green, missing files highlighted red
    # Video Extra Files.xlsx: List of files found that don't match the run log. This script uses pattern matching to find similar files to the desired,
        # but this list is files that include bad typos or files that are in the wrong folders.
# File structure for videos:
    # 1Video/
        # Top/ MCF, AVIs Uncompressed, and AVIs Compressed
        # Side/ MCF, AVIs Uncompressed, and AVIs Compressed
        # Oblique/ MCF, AVIs Uncompressed, and AVIs Compressed

# To use this code:
    # Have the same file structure as above
    # Create a run log of the desired file names that matches "\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video\Video Log.xlsx"
    # Adjust root folder

import os
import pandas as pd
import re
from VideoLog import highlight_excel, create_log # Custom functions for creating/modifying the runlog excel sheet

# Adjustable parameters
    # Change for a different project
root_folder = r'\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video'
excel_file_path = root_folder + r'\Video Log.xlsx'
output_excel_path = root_folder + r'\Video Extra Files.xlsx'
subfolder_names = ['Top', 'Side', 'Oblique']
subsubfolder_names = ['MCF','AVIs Compressed','AVIs Uncompressed']

# This code uses pattern matching to catch some basic typos
pattern_on_off = 1 # Make 1 if you want to use, make 0 if you want to turn it off
    # Change this line of code in the loop below: pattern = re.compile(rf'FieldTurf_2023_{subfolder}[-_]?Run{runIdx}\b',re.IGNORECASE) for different file names

# Load the Run Log
video_log = pd.read_excel(excel_file_path)

create_log() # Creates a copy of the run log for highlighting, Video Log Highlighted.xlsx

file_list = {}
file_count = 0

# Iterate through the run log, checking if each file exists
for runIdx, rowData in video_log.iloc[3:].iterrows(): #iloc[3:] skips the 1st two rows since they are the column names/groups

    c_idx = 0 # c_idx is the column index of the excel file. There are 9 columns: 3 file types (MCF/AVI/AVI Compressed) x 3 camera angles (Top/Side/Oblique) 
    
    for subsubfolder in subsubfolder_names:    
        # file_list[subsubfolder] = {}
        if subsubfolder not in file_list:
            file_list[subsubfolder] = {}
            
        if subsubfolder == 'MCF':
            file_extension = '.mcf'
        else:
            file_extension = '.avi'
        for subfolder in subfolder_names:
            run_name = video_log.at[runIdx,video_log.columns[c_idx]]

            file_path = os.path.join(root_folder, subfolder, subsubfolder, (run_name + file_extension))

            directory_path = os.path.join(root_folder, subfolder, subsubfolder)

            # This generates a list of all the files in each of the 9 subfolders
                # Used for generating a list of files that aren't a match with any of the expected runs
                # This should capture mislabeled videos that need to be manually renamed
            if runIdx == 3: # Only need to generate this list once, so generated on the first past through of the run log
                file_list[subsubfolder][subfolder] = {}
                file_list[subsubfolder][subfolder] = [file for file in os.listdir(directory_path) if file.endswith(file_extension)]

            c_idx += 1

            file_exists = os.path.exists(file_path)

            # This section captures files that have typos in the file name

            # If the filename matches the run number and a similar format, it is counted.
                # General format is: FieldTurf_2023_Side-Run253.mcf
                # This process captured 400+ files that had typos etc.
            pattern = re.compile(rf'FieldTurf_2023_{subfolder}[-_]?Run{runIdx}\b',re.IGNORECASE)
                # rf = formatted raw string)
                # [-_]? means it will accept a -, _, or nothing there to match

            files = [file for file in os.listdir(directory_path) if file.endswith(file_extension)]
            if not file_exists and pattern_on_off:
                for file in files:
                    if pattern.match(file):
                        run_name_found = file
                        file_exists = 1
                        file_path = os.path.join(root_folder, subfolder, subsubfolder, run_name_found)

            # This section updates the run log with green or red highlights if the files exist or not
            if file_exists:
                file_count += 1
                color = '00FF00' # Green

                # If the file does exist, remove it from the list of extra files found in the folders    
                file_name = os.path.basename(file_path)
                print(file_name) 
                file_list[subsubfolder][subfolder].remove(file_name)
            else:
                color = 'FF0000' # Red
            highlight_excel(runIdx,c_idx,color)

print('files found: ' + str(file_count))

#### Extra Files
# Create an excel file that displays the names of extra files in the folders that weren't found by the run log
# This will generate a list of files that need to be renamed manually (i.e. didn't match the pattern closely enough) or don't belong in the folders

extra_files = pd.DataFrame()

# Determine the maximum length of the lists for padding
max_length = max(len(files) for subfolder_files in file_list.values() for files in subfolder_files.values())

for subsubfolder in subsubfolder_names:
    for subfolder in subfolder_names:
        column_name = f"{subfolder} {subsubfolder}"

        # Pad the lists with None to make lengths consistent      
        files = file_list[subsubfolder].get(subfolder, []) + [None] * (max_length - len(file_list[subsubfolder].get(subfolder, [])))

        extra_files[column_name] = files

extra_files.to_excel(output_excel_path, index=False)




  