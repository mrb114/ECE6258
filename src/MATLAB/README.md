# MATLAB Applications and Scripts

This directory contains two applications that assess image quality.  The first, Artifact Detection Application (adapp), is a subjective image quality assessment GUI.  The second is an objective IQ assessment function: runIQMetrics.

Artifact Detection Application
------------
This MATLAB application allows users to assess for the presence and severity of image artifacts in a set of images. The application builds a spreadsheet of user responses that can be used to determine artifact detectability and severity.  These measures can then be correlated with objective image quality metrics to determine the objective image quality features that correlate with subjective responses.

A demo of this application is configured to run from this repository. Simply clone the repository and execute `AppDemo.m` in MATLAB.

To create your own test sequence, create an input file similar to `imageinfo.xlsx` in this directory.  This table allows you to define sets of images and provide their filenames.  Organize these images into a single folder.  You may use a run script similar to `AppDemo.m` to run the application; set the input and output filename parameters according to your created input file and desired output file. Finally, run the script to start the application.

IQ Metrics
------------
This MATLAB function computes image quality metrics for pairs of images provided in an input file, and writes the results to file.  

This code references the UNIQUE and MS-UNIQUE IQ algorithms, used with permisison from Mohit Prabhushankar.

To run, create an input file similar to "imageinfo.xlsx" in this directory. Then open IQDemo.m and set the input and output filename parameters. Finally, run the script. This should reproduce the results found in the final term paper.

Calculation of the aggregate statistics (found in the paper) was performed in Excel. For each metric column, the mean (Excel function AVERAGE) and sample standard deviation (STDEV.S) were calculated.
