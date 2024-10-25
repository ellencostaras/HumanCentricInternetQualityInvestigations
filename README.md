# Human Centric Internet Quality Investigation

Welcome to the living appendix for 'Are Australian Metrics of Internet Quality Sufficiently Human-Centirc?',
a thesis submitted to the Faculty of Science, Monash University for the degree of Bachelor of Science Advanced - Global Challenges (Honours). 

Authors: Ellen Costaras, Aadya Mishra, Aden Strong. 

This repository includes all of the code, raw data, cleaned data, and analysis for Chapters 2, 4, and 5 of the thesis, and all of the code from Chapter 3. 

## Lab and Field Experimentation folder:

This folder houses code and data from Chapters 2, 4 and 5. This includes:
- 'lab_automation.ipynb', the script for automating lab experiments
- 'field_automation'.ipynb', the script for automating field experiment
- 'pre_experiment' the files creating the internet conditions to test 
- 'post_experiment', includes the data from WebRTC, and scripts to parse, clean and analyse the data.

## Latency Data Analysis folder:

This folder includes the scripts for analysing data used in our study. It does not include the data itself. This includes:
- 'ADM_to_LGA.ipynb', the initial treatment of Monash IP Observatory data and conversion to LGA subdivision
- 'linear_regression.ipynb', the spatial join of independent variables
- 'normalcy_check.ipynb', the check that data does not violate linear assumptions
- 'latency_regression_trimmed.ipynb', the regression analysis of latency correlates
- 'comparison.ipynb', the comparison between Monash IP Observatory data and MBA data
