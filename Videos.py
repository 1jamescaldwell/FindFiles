# James Caldwell
# University of Virginia, Center for Applied Biomechanics
# January 2024

import os
import pandas as pd
import re

from VideoLog import highlight_excel, create_log

# Path to the root folder
root_folder = r'\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video'

# Path to the Excel file
excel_file_path = r'\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video\Video Log.xlsx'

# Load the Excel file into a pandas DataFrame
video_log = pd.read_excel(excel_file_path)

create_log()

file_list = {}
file_count = 0

# Iterate through the run log, checking if each file exists
for runIdx, rowData in video_log.iloc[3:].iterrows(): #iloc[3:] skips the 1st two rows since they are the column names/groups

    c_idx = 0 # c_idx is the column index of the excel file. There are 9 columns: 3 file types (MCF/AVI/AVI Compressed) x 3 camera angles (Top/Side/Oblique) 
    for subsubfolder in ['MCF','AVIs Compressed','AVIs Uncompressed']:
        
        if subsubfolder == 'MCF':
            file_extension = '.mcf'
        else:
            file_extension = '.avi'
        for subfolder in ['Top', 'Side', 'Oblique']:
            
            file_list[subfolder] = {}

            run_name = video_log.at[runIdx,video_log.columns[c_idx]]

            file_path = os.path.join(root_folder, subfolder, subsubfolder, (run_name + file_extension))
            # left off here
            directory_path = os.path.join(root_folder, subfolder, subsubfolder)

            # file_list[subfolder][subsubfolder] = {}

            file_list[subfolder][subsubfolder] = [file for file in os.listdir(directory_path) if file.endswith(file_extension)]
            print(file_list['Top']['MCF'])

            files = [file for file in os.listdir(directory_path) if file.endswith(file_extension)]

            c_idx += 1

            file_exists = os.path.exists(file_path)

            # Define the regular expression pattern
            pattern = re.compile(rf'FieldTurf_2023_{subfolder}[-_]?Run{runIdx}\b',re.IGNORECASE)
                # rf = formatted raw string)
                # [-_]? means it will accept a -, _, or nothing there to match
                # (\d+) is digits 

            if not file_exists:
                for file in files:
                    if pattern.match(file):
                        run_name_found = file
                        file_exists = 1
                        file_path = os.path.join(root_folder, subfolder, subsubfolder, run_name_found)

            # 645 found best 
            # Doing match pattern found 1023
            # Next: need to generate list of files found that have no matches
            # Also, update excel with highlights or missing values
            if file_exists:
                print(file_path)
                file_count += 1
                color = '00FF00' # Green
            else:
                color = 'FF0000' # Red

            highlight_excel(runIdx,c_idx,color)
            
print('files found: ' + str(file_count))

  