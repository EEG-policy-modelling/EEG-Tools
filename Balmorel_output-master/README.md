# README #

### What is this repository for? ###

This README tells you how to process Balmorel results by sql-queries that can be executed from a python script or VBA with the help of the files in this repository.

### How do I get set up? ###

## Prerequisites
- GAMS version 2x.x or later which includes the gdx2sqlite utility (TO BE SPECIFIED: might be 24.3 but needs verification)
- Python or MS Excel software
- Output from Balmorel which is either in classical BB1/BB2/BB3 format in regards of output data domains. For example, the domains of VGE_T in BB1/BB2/BB3 are (in this order): Case, Year, Area, Technology, Season, Timestep. In BB4 the domains are: Case, Year1, Year2, Area, Technology.  In case of any deviation from the number of domains or the order of domains the queries will not be functional.
- Output from Balmorel in a single .gdx file which includes both output equations and variables as well as sets and parameters used as input. OR in a .db file

## Creating the SQLite database directly from Balmorel run
* in balmorel.opt set yes for $setglobal MERGEDSAVEPOINTRESULTS2SQLITE

## Creating the SQLite database from a Balmorel output
If you do not get the .db file directly from the Balmorel run, you can also convert it afterwards:
* Convert the Balmorel output gdx-file to a sqlite file with the ending .db following this [explanation of using gdx2sqlite](https://www.gams.com/latest/docs/userguides/mccarl/gdx2sqlite.htm). More detailed explanation: Open a terminal (in windows: search for 'cmd'). Then type
cd.. <Enter>
cd.. <Enter>
cd win64 <Enter>
cd 24.4 <Enter>
gdx2sqlite -i <filepath of the gdx-file> -o <filepath of the sqlite-output-file> 
e.g. gdx2sqlite -i c:\users\frwi\documents\...\BASE-results.gdx -o c:\users\frwi\documents\...\BASE-results.db

* Clone this repository
* Open either the Python script (.py) (not existing yet) on your computer or open the VBA-file, press the button, choose the path of the .db file and happily play with the results

## Setting up Python

*maybe filled in by Frauke

## Setting up Excel/VBA

1) The SQLite3 ODBC driver for Excel needs to be installed. It is crucial to install the correct version (32 or 64 bit) according to the system used. 
The 32-bit version is available at: http://www.ch-werner.de/sqliteodbc/sqliteodbc.exe .
In a 64 bit operating system and a 64-bit software package, the 64-bit version of the drivers can be used: http://www.ch-werner.de/sqliteodbc/sqliteodbc_w64.exe
2) In VBA, ActiveX library has to be activated. From top menu: Tools -> References -> Microsoft ActiveX Data Objects X.X Library (where X.X stands for the newest version available)
 
### Contribution guidelines ###

The SQL commands used to manipulate data are created and improved according to the needs of the users. In case of specific requests, broken SQL commands or questions, please refer to Hardi or Frauke
* To be continued
* Still missing: Choice of not executing all sql-queries (takes time) by ordering blocks of sql-queries and necessary in any case and other sql-queries / pictures for the python version / Make it run for postgreSQL-database

### Who do I talk to? ###

### User's manuals for output tools

## Python

## Excel/VBA

Control over the VBA script to the user is provided in the sheet Choose Database. There, several options are present and execution buttons can be found.

1) Control "Query Type to use" refers to the structure of the output database. In a traditional BB1/BB2/BB3 model, the output varibales have one year index. In the new BB4 output format, two year indecis are present, needing a different kind of queries. Using the wrong option here will cause a non-informative error from VBA while attempting to execute the queries.
2) "Queries to Execute" allows the user to execute specific or all data manipulation queries. Data will be available in Excel for only the data types chosen here.
3) Option to limit the output manipulated by only selecting data for some countries (relevant only for very large database tables, i.e more than 10M rows)
4) Select database + Run Queries
5) Go into a sheet, select "Data" and click "Refresh all" - otherwise the new results do not show up


* Hardi or Frauke
* others?