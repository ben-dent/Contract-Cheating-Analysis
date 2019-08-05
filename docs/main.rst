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

This function sets up the program and then executes it. It creates the database and then calls *getSeen*.
After this, it uses *getAllTheRelevantLinks* to fetch all the project URLs and then runs *fetchDataNonLogin* on each of them that has not been seen before.

After running *fetchDataNonLogin*, the program will have retrieved the winner details so this function then calls *lookAtWinnerProfiles* to get all the details.

Creating database tables
*************************

databaseSetup
______________
.. code-block:: python

   databaseSetup()

This function creates all the tables in the database (if they do not yet exist) by calling the relevant function.

createWinnersTable
____________________
.. code-block:: python

   createWinnersTable()

Creates the Winners table in the database, which will initially be empty.

createQualificationsTable
_____________________________
.. code-block:: python

   createQualificationsTable()

Creates the Qualifications table in the database, which will initially be empty.

createReviewsTable
______________________
.. code-block:: python

   createReviewsTable()

Creates the Reviews table in the database, which will initially be empty.

createJobsTable
__________________
.. code-block:: python

   createJobsTable()

Creates the Jobs table in the database, which will initially be empty.

createJobsHourlyTable
__________________________
.. code-block:: python

   createJobsHourlyTable()

Creates the JobsHourly table in the database, which will initially be empty.

createProfilesTable
______________________
.. code-block:: python

   createProfilesTable()

Creates the Profiles table in the database, which will initially be empty.

createBidsTable
__________________
.. code-block:: python

   createBidsTable()

Creates the Bids table in the database, which will initially be empty.

Program Execution
^^^^^^^^^^^^^^^^^^^^^

lookAtWinnerProfiles
---------------------
.. code-block:: python

   lookAtWinnerProfiles()

This function logs into Freelancer by calling the *loginToFreelancer* function and then calls the *getInformationFromBidderProfile* function, passing in the profile URL, to retrieve all the relevant data from that profile.
It then adds the given profile to the profiles already seen, to prevent duplication within a single program execution.

Saving to database
*******************


