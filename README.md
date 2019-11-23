# Animal Data Viewer

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

# Animal Data Path folder structure:  

    .Animal Data folder
    ├── ...
    ├── Experiment Name folder     # Folder containing all data for an experiment set.
    │   ├── D5                     # Day number of the measurement
    │       ├── integration         # End-to-end, integration tests (alternatively `e2e`)
    │       └── unit                # Unit tests 
    │
    │
    │
    ├── Another Experiment 
    └── ...
    



`
|-D5 / D7 etc.  
  |-FP  
  |- Monkey Number  
     |- XXXXXXX-L.jpg  
     |- XXXXXXX-R.jpg         
       
  |-OCT    
  
    |- Monkey Number      
    
       |-OD    
       
         |- XXXXXX.jpg    
         
       |-OS    
       
         |- XXXXXX.jpg  
         `

JSON file path is for saving indexing file of data. 
App will scan for any folder changes, reindex experiments folder changes and save index info of each experiment to a JSON file.

The settings of both folders are in the settings.json file. 

