Main.py
========

This is the main file of the program and consists of a single class, Main.
The constructor of this class initialises the GUI and also any attributes to ensure visibility throughout the Main class.

This file imports the *Crawler.py* and *DataAnalysis.py* files in order to execute their various functions.

In addition to using the functions from these two files, it has a number of its own functions.

Setup
^^^^^^^^^

These functions are concerned with setting up the program and are called at the beginning of execution, if they are needed.

getSeen
--------
.. code-block:: python

   getSeen()

This function retrieves the jobs and profiles already seen from the database and updates a dictionary to hold their IDs.
This prevents data duplication and wasted time retrieving data already seen.

setUpProgram
-------------
.. code-block:: python

   setUpProgram()

