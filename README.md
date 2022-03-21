# microplastics_boxmodel

2022/03/21 Alkuin Koenig

Microplastics box model.  
Its best to clone the whole project and maintain its folder structure, because this way the relative paths should just work (absolute paths stink).  


- Python code in /Spyder_proj/microplastics/scripts
- the "main script" is "boxmodel_V1.py". This script will take a .json input file for the parameters (k values, etc) and will output a .csv file with the results. There is an option to also include the used parameters in the output as metadata.
- forcing functions (plastic produced, plastic recycled, etc) are in boxmodel_forcings.py. They should get automatically imported when you run "boxmodel_V1.py". (Unless you were naughty and didn't maintain the folder structure)
- input files in .json format can be found in /input. You can change values in these values (should be fairly self explaining), but if you do so rename the new file.
- you have to pass the .json input file you want to use to "boxmodel_V1.py" by name (the file has to be found in /input).
- The output of "boxmodel_V1.py" will be saved automatically as .csv in /output. Output file names will be generated automatically and will depend on your system time when the script was run, as well as the input file that has been used.
- an example script to plot output in /Spyder_proj/microplastics/scripts named "plot_model_results.py". You need to feed this script a "model output .csv" file, as created by "boxmodel_V1.py".
- Jeroens Excel model as well as "historical plastics production and waste generation" can be found in /Excel
- /archive is the dumping ground. Probably we won't need stuff in there, but I left it just in case.
- In /info I have put articles and other non-top-secret-stuff that was sent around. We'll probably don't need that folder so it might dissappear at some point.
