# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 13:20:57 2019

@author: tilseb@dtu.dk

Based on previous work by Elaine T. Hale (https://pypi.org/project/gdxpds/) and
Philipp Andreas Gunkel (DTU).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

#
# PREREQUISITES
#

# importing required packages and modules (keep order)
import os
import config
import datetime
import glob
import gdxpds as gp
import pandas as pd

# path to the local gams installation
gams_dir = config.local_gams

# project name
pr_name = config.project_name

# directory to the input gdx file(s)
gdx_file_list = glob.glob('input/*.gdx')

# create output directory
if not os.path.isdir('output'):
    os.mkdir('output')


#
# VARIABLE SPECIFICATION
#

# load the variable specification table that defines which varaibles will be
# included and the index names for each variable.
var_specs = pd.read_csv('variable_specification.csv',
                        encoding='utf8')

# drop all variables that shall NOT be included and set the index to the
# variable names
var_specs = var_specs[var_specs.include == 'YES']
del var_specs['include']
var_specs = var_specs.set_index('variable')

# list of all variable names
var_list = var_specs.index


#
# DATA PROCESSING
#

# create for each variable a dataframe that merges the variable data of all gdx
# files and write it to an excel file
for varname in var_list:

    """ loop through the variable list and create an empty dataframe in each
    iteration.
    """

    data = pd.DataFrame()

    for gdx_file in gdx_file_list:

        """ loop through the gdx file list and load the data in an empty
        temporary dataframe. Concatenate the temporary dataframes in each
        iteration. Finally, write the concatenated dataframes to a singel excel
        file that is named by the variable name.
        """

        # check, if scneario is defined
        if '_' in gdx_file:
            # if yes: extract scenario name from gdx filename
            scenario = gdx_file.split('_', 1)[-1][:-4]
        else:
            # if no: use nan instead
            scenario = 'nan'

        # print iteration progress
        print('MainResults: ' + scenario + '\n'
              'Variable: ' + varname)

        # creat empty temporary dataframe and load the gdx data into it
        temp = pd.DataFrame()
        temp = gp.to_dataframe(gdx_file, varname, gams_dir=gams_dir,
                               old_interface=False)

        # extract the new column names from the variable specification table
        # and overwrite the old ones with them;
        temp.columns = list(var_specs.loc[varname]
                            .index[var_specs.loc[varname]])

        # add a scenario column with the scenario name of the current iteration
        temp['Scenario'] = scenario

        # put the scenario column in first position
        cols = list(temp.columns)
        cols = [cols[-1]] + cols[:-1]
        temp = temp[cols]

        # concatenate the temporary dataframe to the preceeding data
        data = pd.concat([data, temp], sort=False)

    # print excel file creation progress
    print('Writing data to excel worksheet for variable: ' + varname)

    # create time stamp with current local time in the format (yymmdd-HHMM)
    time = datetime.datetime.now().strftime('%y%m%d-%H%M')

    # path to excel file with the name of the variable in current iteration
    csv_file = 'output/' + pr_name + varname + '_' + time + '.csv'

    # write the data to a csv file
    data.to_csv(csv_file, encoding='utf8', index=False)


# print final statement
print('End of execution.')


# = END =======================================================================
