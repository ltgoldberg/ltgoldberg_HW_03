I. My python program collects information from ebay. It will collect what I specifically search for on the site; for instance, the words I searched were "wrentch" "pencil case" and "bicycle". The program then retrieves information for these keywords from ebay. After extracting the proper information, it then converts the it into a library and then makes it into a json file. 

II. These are the codes you should run to generate the 3 json files for "wrentch", "pencil case", and "bicycle". 

```
python3 ebay-dl.py 'wrentch'  
python3 ebay-dl.py 'pencil case'  
python3 ebay-dl.py 'bicycle'  
```

III. 
```
python3 ebay-dl.py 'wrentch'--csv  
python3 ebay-dl.py 'pencil case'--csv 
python3 ebay-dl.py 'bicycle'--csv 

[Course Project] (https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)
