# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:20:43 2017

@author: frwi
"""

# Import necessary packages
import sqlite3
from sqlite3 import OperationalError
import time

# Start timer to keep track of duration of operations
start = time.time()

# Settings
dbName = 'BASE-Results.db'


# Create the connection to the sqlite-file
conn = sqlite3.connect('C:/Users/frwi/Documents/balmorel_output_tests/bb4_test/BASE-results.db')

# Do not know what the c is exactly doing, most code following taken from here:
# http://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
c = conn.cursor()

# Open and read the sql-file as a single buffer
#ToDO: make path and filename-setting easier, with the hel of import os.path (cwd = os.getcwd()  # Get the current working directory (cwd))
#ToDo: see http://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory
fd = open('C:/Users/frwi/Documents/git_repositories/Balmorel_output/QUERY_Out.inc','r')
sqlFile = fd.read()
fd.close()

# Remove blank linebreaks marked as \n
sqlFile = sqlFile.replace("\n","")

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# this is how the commands look like now
sqlCommands

# Execute every command from the input file
for command in sqlCommands:
    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands
    try:
        c.execute(command)
    except OperationalError:
        print("Command skipped: ")
    # Print out timer value after each query execution
    end = time.time()
    print(end - start)
	
    
# Close the connection to the database - otherwise you cannot access the db-file
conn.close()
