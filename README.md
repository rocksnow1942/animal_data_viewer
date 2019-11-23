# Animal Data Viewer  

[![Python Versions][pyversion-button]][md-pypi]  

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg  

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

