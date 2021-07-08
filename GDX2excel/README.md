# GDX2Excel

This script converts one or more variables from .gdx files produced by Balmorel to excel files.
There is also a function to calculate market values.

## Prerequisites

The following software is needed to run the script:

### programming languages
- python 3.6
- Local GAMS installation, tested with version 34

### side packages
- gdxpds
- pandas
- openpyxl
- tkinter
- matplotlib

## Execution

1. Set the path to the local gams installation and the project name in the config.py file.
	> Example: C:/GAMS/34
	>
	> The project name is only used to name the output files.
	
2. Place all gdx files you want to process in the input directory in the project folder or change the path with the option 'c' in the script
	> /input
	
3. Run the script and select one of the options.

4. All excel files for each variable are now in the output folder.

### Options
1. calculate market values and export .xlsx
2. calculate market values and exports market values + EL_Price + VGE_T + QEEQ to excel
3. Manually choose variable from MainResults and export to .xlsx
4. Manually choose variable from Base-results and export to .xlsx
5. Get electricity price for all countries and export to .xlsx
6. Plot VGE_T in stacked area plot

## Additional information
- The script creates separate files for every year in the simulation



to be continued