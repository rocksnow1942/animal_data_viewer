# Animal Data Viewer  

[![python version][pvlogo]][pythonwebsite]
[![2][flg]][flask]
[![advaa][version]][adv]


[pvlogo]: https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20-blue
[pythonwebsite]: https://www.python.org/downloads/release/python-375
[flg]: https://img.shields.io/badge/flask-1.1.1-green
[flask]: https://palletsprojects.com/p/flask/
[version]: https://img.shields.io/badge/version-0.1.0-brightgreen
[adv]: https://github.com/rocksnow1942/animal_data_viewer

### How to use:
* Download repo and extract to a folder. 
* python version > 3.7
* On Mac terminal,
* Install flask package:  
`$ pip install Flask==1.1.1` # tested on this version   
or  
`$ pip install Flask`  
then run  
`$ python your/path/to/app.py `

### Animal Data Path folder structure:  
Animal data files must be organized in following structure for proper indexing.

    . Animal Data folder
    ├── ...
    ├── Experiment 1 folder             # Folder containing all data for an experiment set.
    │   ├── D7                          # Day number of the measurement
    │   │   ├── FP                      # FP measurement folder
    │   │   │   ├── Subject No. 1       # test subject 1; folder name is label. 
    │   │   │   │   ├── XXXXXXX-L.jpg   # FP imgages. -L.jpg means left eye
    │   │   │   │   └── XXXXXXX-R.jpg   # FP imgages. -R.jpg means right eye
    │   │   │   ├── Subject No. 2       # test subject 2; folder name is label. 
    │   │   │   │   └── ...
    │   │   │   └── ...
    │   │   ├── OCT                      # OCT measurement folder
    │   │   │   ├── Subject No. 1 
    │   │   │   │   ├── OD               # OD folder (right eye)
    │   │   │   │   │   ├── XXXXXXX.jpg  # OCT images for OD. 
    │   │   │   │   │   └── ...
    │   │   │   │   └── OS               # OS folder (left eye)
    │   │   │   │       ├── XXXXXXX.jpg  # OCT images for OS. 
    │   │   │   │       └── ...
    │   │   │   ├── Subject No. 2 
    │   │   │   │   └── ...
    │   │   │   └── ...
    │   │   ├── Other measurements       # currently, only index FP and OCT measurements.
    │   │   └── ...               
    │   ├── D15                          # measurements on another day, same structure.
    │   │   └── ...
    │   └── ...
    ├── Experiment 2 folder              # another set of experiment.
    └── ...  
    
### JSON file path 
JSON file path is for saving indexing file of data.
App will scan for any folder changes, reindex experiments folder changes and save index info of each experiment to a JSON file.


The settings of both folders are in the settings.json file. 

