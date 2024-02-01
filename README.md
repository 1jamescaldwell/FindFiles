Project using: complex looping, matching patterns (re library), os, pandas, and excel read/write. 

A test series at my lab conducted ~400 tests. Each test has three camera angles. Each video has a raw format (.mcf), converted format (.avi), and compressed format (.avi compressed). Thus, the team needed to organize, save, convert, and document a total of 4000+ video files. I wrote this script to generate a list of the files that were saved/completed and which files were missing. 

VideosMain.py is the main <br>
VideosLog.py is a function for creating/modifying/highlighting excel log sheets <br>

Inputs: This script takes in a run log, Video Log.xlsx <br>
Outputs: The script creates 2 excel files:  <br>
    `&#9;` Video Log Highlighted.xlsx: The same as the original video log, modified for all files that exist highlighted green, missing files highlighted red <br>
    `&#9;` Video Extra Files.xlsx: List of files found that don't match the run log. This script uses pattern matching to find similar files to the desired, but this list is files that include bad typos or files that are in the wrong folders.
