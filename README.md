### Python Assessment

An assessment for a Python development position. I'm leaving out the details of the prompt to reduce
the chances of this repo showing up in searches performed by candidates who haven't solved the problem
themselves yet.

##### Overview

To run the script, edit the mysql connection parameters at the top of `main.py`,
then run it with a Python 2.7 interpreter. It should first create the tables, views, and the
procedure, then populate them with data, run the queries, and print the results.

I approached this task with the objective of making the program as turn-key as possible, so I added
some things that I wouldn't want in a production environment. For example, I probably wouldn't normally
drop database artifacts every time a script is run, but doing so simplifies the script's operation.

##### Contents

* [csv](csv): the csv files used to populate the tables
* [python](python): the python source files
    * main.py: the main, runnable file
    * inserter.py: a sql utility to insert rows into a db
    * transformation.py: a class to perform the custom transformation
    * scoretests.py: unit tests
* [sql](sql): the sql files. All of them are used except for `top-coach-players-inline.sql`, which
is just `top-coach-players.sql` with the views inlined.
* [output.txt](output.txt): output of the script when I ran it

