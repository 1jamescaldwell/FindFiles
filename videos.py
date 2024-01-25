import os
import pandas as pd
import re

# Path to the root folder
root_folder = r'\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video'

# Path to the Excel file
excel_file_path = r'\\cab-fs07.mae.virginia.edu\NewData\FieldTurf\2023-FieldTurf\1Video\Video Log.xlsx'

# Load the Excel file into a pandas DataFrame
video_log = pd.read_excel(excel_file_path)

i = 1
file_count = 0

for runIdx, rowData in video_log.iterrows():

    # print(video_log.at[runIdx,video_log.columns[0]])
    # print(video_log.columns[0])
    c_idx = 0
    for subsubfolder in ['MCF','AVIs Compressed','AVIs Uncompressed']:
        
        if subsubfolder == 'MCF':
            file_extension = '.mcf'
        else:
            file_extension = '.avi'
        for subfolder in ['Top', 'Side', 'Oblique']:
            
            run_name = video_log.at[runIdx,video_log.columns[c_idx]]
            
            
            # pattern = re.compile('FieldTurf_2023'+[-_ ]?, re.IGNORECASE)
            # pattern = re.compile(r'FieldTurf_2023_subfolder[-_]?runIdx(\d+)')
            # pattern = re.compile('FieldTurf_2023_Top-Run1')







            file_path = os.path.join(root_folder, subfolder, subsubfolder, (run_name + file_extension))
            
            directory_path = os.path.join(root_folder, subfolder, subsubfolder)
            # print(directory_path)
        #Original files
            files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
        # New files
            files = [file for file in os.listdir(directory_path) if file.endswith(file_extension)]


             # Define a regular expression pattern to match variations in the run number
            # pattern = re.compile(f"{re.escape(run_name)}[-_]?Run\d+{re.escape(file_extension)}", re.IGNORECASE)
            
            # print(directory_path)
            # for filename in os.listdir(directory_path):
                            
                # file_path = os.path.join(root_folder, subfolder, subsubfolder, filename)

                # file_path = os.path.join(root_folder, subfolder, subsubfolder, (run_name + file_extension))
                # Check if the filename matches the pattern
                # if pattern.match(filename):
                    # print(file_path)
                    # file_count += 1

            c_idx += 1

            file_exists = os.path.exists(file_path)

            # Define the regular expression pattern
            pattern = re.compile(rf'FieldTurf_2023_{subfolder}[-_]?Run{runIdx}\b',re.IGNORECASE)
                # rf = formatted raw string)
                # [-_]? means it will accept a -, _, or nothing there to match
                # (\d+) is digits 


            if not file_exists:
                for file in files:
                    # print(file)
                    if pattern.match(file):
                        run_name_found = file
                        file_exists = 1
                        file_path = os.path.join(root_folder, subfolder, subsubfolder, run_name_found)
                        # print(file)

                        
                # print(run_name)
                #     # file_count += 1

            # 645 found best 
            # Doing match pattern found 1023
            # Next: need to generate list of files found that have no matches
            # Also, update excel with highlights or missing values
            if file_exists:
                print(file_path)
                file_count += 1

            
print('files found: ' + str(file_count))

# print(files)
  