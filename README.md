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
.
+-- _config.yml
+-- _drafts
|   +-- begin-with-the-crazy-ideas.textile
|   +-- on-simplicity-in-technology.markdown
+-- _includes
|   +-- footer.html
|   +-- header.html
+-- _layouts
|   +-- default.html
|   +-- post.html
+-- _posts
|   +-- 2007-10-29-why-every-programmer-should-play-nethack.textile
|   +-- 2009-04-26-barcamp-boston-4-roundup.textile
+-- _data
|   +-- members.yml
+-- _site
+-- index.html

Experiment Name Folder


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

