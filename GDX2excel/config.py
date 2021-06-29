# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:50:13 2019

@author: tilseb

This is the config file of the mainresults_2_excel script.
Here the user can define global settings and variables.
"""

# path to the local gams installation
local_gams = 'C:/GAMS/34'
#print('GAMS installation: ' + local_gams)

# project name (if no project name shall be specifified put only '')
project_name = 'test_aures2'
if project_name:
    #print(project_name)
    project_name += '_'
else:
    print('No project name defined. See config.py settings.')
