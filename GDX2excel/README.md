# GDX2CSV

This application converts one ore more variables from .gdx files produced by Balmorel to excel files.
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

## Execution

1. Set the path to the local gams installation and the project name in the config.py file.
	> Example: C:/GAMS/34
	>
	> The project name is only used to name the output files.
	
2. Place all gdx files you want to process in the input directory in the project folder
	> /input
	
3. Run the script
	Select one of the options.

4. All excel files for each variable are now in the output folder.

## Additional information
- The script creates separate files for every year in the simulation
