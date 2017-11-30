% Demo script to run adapp

clear; close all;

% Create app
app = adapp;

% Set app input/output files
app.imagedir = '../../Images/IQDev/';
app.metafilename = 'imageinfo.xlsx';
app.resultsfilename = 'results.xlsx';

% Run app
app.run();