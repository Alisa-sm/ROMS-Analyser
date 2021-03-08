# ROMS-Analyser

A new data analysis framework where Routine Outcome Measures (ROMS) are analysed to assess the efficacy of low intensity therapeutic interventions. 

In order to run these scripts locally, please ensure that you have python installed. 

## File Structures

- Within the notebooks folder, you will find the jupyter notebook versions of various scripts. If you prefer to use jupyter notebook as your text editor, please feel free to use those.
- roms_analyser.ipynb = customised script to analyse cwp/emhp outcome data.
- roms_reliable_change.ipynb = calculates reliable change for each outcome measure dataset.
- site_reports.ipynb = the script use to generate site reports analysis.
- swl_data_analysis.ipynb = detailed analysis on a site (swlnhs trust).
- Procfile = heroku configuration file.
- README.md = information about the code project.
- index.py = streamlit code responsible for the web application interface. Changes to index.py will affect the web application interface. 
- reliable_change.py = python version for reliable change algorithms.
- requirements.txt = libraries used (and version number). 
- setup.sh - heroku setup

## Updating the web application

If you need to make any changes to the web application (e.g. update features or fix bugs), you can do this by editing the index.py file. My suggestion would be to load this to your local environment/machine. Once you have made your changes and are happy that they work, push those changes here (to the main branch or another branch, doesn't really matter) and let me know (arifiya96@gmail.com). I will pull those changes to the heroku server :) 

### References

Reliable change algorithms for RCADS, SDQ and GBO from Edbrooke et al (2016)
https://link.springer.com/content/pdf/10.1007/s10488-014-0600-2.pdf 

Link to site report generator https://site-report-generator.herokuapp.com/
