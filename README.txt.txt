1. 1.  FILE STRUCTURE & DESCRIPTION 
            /CODE
                /Indicators
                /N-gram IDF
                /RAKE
        /DATA_VISUALIZATION
                /data
                /js
                /scripts
                /index.html
                /rader.html
                /word_cloud_season
        /DOC
                /team06poster.png
                /team06report.pdf
        /README.txt
                
        Under CODE directory:
        #####
        Important: All source codes under CODE need to be run with the original data files. We 
        do not upload the data files due to their sizes. 
        #####
RAKE: All .ipynb files in RAKE are codes of tests based on python-rake package  https://pypi.python.org/pypi/python-rake  . seasons_trt.ipynb/years_trt.ipynb, 
are tests based on four seasons/ six years AIrbnb review data of Toronto.  Wiki-trt-all-method.ipynb are based on description text of Toronto from Wikipedia.Tests performes on different stopwords list and paprameters of RAKE.
1. 2. INSTALLATION
        For everything under DATA_VISUALIZATION file, firefox is required to load them locally.
 
If you want to run our data analysis code: Install R/Rstudio. Packages include: readxl, reshape2, ggplot2, devtools, ggbiplot, cluster, caret
RAKE: Install Python 2.7, python-rake, Jupyter Notebook. 
N-gram IDF: Python 3 required. Python packages include: Numpy, Textblob,Pandas


1. 3. EXECUTION
        Open the html files under DATA_VISUALIZATION using firefox.


1. DATA SOURCE
        Indicator calculation: https://knoema.com/
        Airbnb comments: http://insideairbnb.com