Work in progress 1/25/24

Project using: complex looping, matching patterns (re library), os, pandas, and excel read/write. 

A test series at my lab conducted ~400 tests. Each test has three camera angles. Each video has a raw format (.mcf), converted format (.avi), and compressed format (.avi compressed). Thus, the team needed to organize, save, convert, and document a total of 4000+ video files. I wrote this script to generate a list of the files that were saved/completed and which files were missing. 

Videos.py is the main
VideosLog.py is a function for creating/modifying/highlighting excel log sheets
