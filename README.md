# Circulating miRNA and lung cancer: - an analysis of available data

This repository contains all the code that was used to create the master thesis: `Berg, O.F.B.: Circulating miRNA and Lung Cancer: - a More Comprehensive Analysis of Available Data. NTNU Open (2022)`. Below is a description of the repository.

## `/Data manipulations`

This directory contains all manipulation of data that was done in this project.

### `/Data manipulations/Dataset`

A directory that contains all raw data files from the different studies. Note: this folder is not populated in this repository due to lack of rights.

### `/Data manipulations/Notebooks`

Here are the [Jupiter notebooks](https://jupyter.org/) that were used for reading in the raw data files and processing them into a common format. The name of the notebook corresponds to the name of the dataset that was processed. Running the notebooks from top to bottom will convert the dataset correctly.

### `/Data manipulations/Others`

A folder with miscellaneous files that are used in the data manipulation. Mostly files that concerns files that are used for converting between different miRNA identifiers.

### `/Data manipulations/Scripts`

This is a folder with all the scripts that have been used for calculating results in this master thesis. Especially note that it contains a `Utils` folder that contains helper scripts for reading datasets and converting between miRNA identifiers.

### `/Data manipulations/Outdata`

This is the folder where the scripts in the `/Data manipulations/Scripts` folder store their results.

### `/Data manipulations/TransformedData`

This is the folder where the notebooks in the `/Data manipulations/Notebooks` store the datasets that have been normalized and converted. Note: this folder is now empty, but the normalized data can be found at [https://doi.org/10.5281/zenodo.6568980](https://doi.org/10.5281/zenodo.6568980).

### `/Data manipulations/build_project.sh`

Is a shell script that automatically runs all the scripts that calculates results for the master thesis and copies the results to the `/Masterthesis` folder so that the new results will automatically be read into master thesis.

## `/Webapp`

This is the folder where the data visualization tool is.

### `/Webapp/computations`

This is a folder with scripts that precomputes all the necessary computation for the visualization tool. `run_computations.sh` is a shell script that runs all the scripts, so that all the necessary computations will be done running only this shell script. `Outdata` is the folder where all the results of the computations are stored.

### `/Webapp/data-visualizer`

This is the folder for the web page of the data visualization tool. It is built using [Node.js](https://nodejs.org/en/) and [React](https://reactjs.org/). To run the application one has to install Node.js. Then, inside this directory, run:

`npm install`

and finally

`npm run start`

Then the web application will run at [localhost:3000](https://localhost:3000).

The code of this website is in the `src` folder which has a structure as follows:
- `App.js` is the main file for defining the web page
- `Datasets.js` keeps track of the name of the datasets
- `Routes.js` is a file that defines the routing of the components in this web application
- `index.css` is a CSS file for defining the appearance of the web application
- `components` is a folder with all the different components in the web application

## Preparation project and Master thesis

The `/Preproject` and `/Masterthesis` directories are for the preparation project report and the master thesis, respectively. The directories have similar structures. It is important to note that the reports are using [`pythontex`](https://github.com/gpoore/pythontex), which means that `pythontex` has to be run when compiling. See `clean_compile.sh` for an example of how.

- `bibtex` is a folder where the file with the references is
- `figs` is a folder with all the figures that is used in the report
- `sections` is a folder with all the different sections of the report
- `tables` is the folder with all the results are stored, that are automatically read into the report when compiling the report
- `main.tex` is the main Latex file, that reads in all the other Latex files, and is the file that should be compiled
- `setup.tex` is a Latex file with all setup options and libraries that are used in the project, and is automatically read by `main.tex`
- `clean_compile.sh` is a helper shell script that provides a clean new compilation of the report including rerunning `pythontex`
- `main.pdf` is the resulting compiled report.

