# MATLAB Applications and Scripts

This directory contains two applications that assess image quality.  The first, Artifact Detection Application (adapp), is a subjective image quality assessment GUI.  The second is an objective IQ assessment function: runIQMetrics.

Artifact Detection Application
------------
This MATLAB application allows users to assess for the presence and severity of image artifacts in a set of images. 

To get started, create an input file similar to "imageinfo.xlsx" in this directory.  Then open AppDemo.m and set the input and output filename parameters. Finally, run the script to start the application.

IQ Metrics
------------
This MATLAB function computes image quality metrics for pairs of images provided in an input file, and writes the results to file.  

To run, create an input file similar to "imageinfo.xlsx" in this directory. Then open IQDemo.m and set the input and output filename parameters. Finally, run the script.

This code references the UNIQUE and MS-UNIQUE IQ algorithms, used with permisison from Mohit Prabhushankar.