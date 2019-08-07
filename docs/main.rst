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

Program Execution - Logged out
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fetchDataNonLogin
------------------
.. code-block:: python

   fetchDataNonLogin(url)

This function looks at the given project web page and fetches all the relevant data from this, including information about bids and bidders. It calls many other functions from this class and the other files in the program.
It takes 1 argument:

| - *url*: This is the url of the project that is being looked at.

getCustomerCountry
-------------------
.. code-block:: python

   getCustomerCountry()

This function returns the country of the customer who posted the project currently being looked at.

getBiddersInfo
---------------
.. code-block:: python

   getBiddersInfo(url)

This function gets all information about the bidders then calls *getBiddersCountries* to get their locations.
It takes 1 argument:

| - *url*: This is the url of the project that is being looked at.

getBiddersCountries
--------------------
.. code-block:: python

   getBiddersCountries()

This function retrieves the countries of the bidders of the project being currently looked at and stores them in a dictionary

Program Execution - Logged in
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lookAtWinnerProfiles
------------------------
.. code-block:: python

   lookAtWinnerProfiles()

This function logs into Freelancer by calling the *loginToFreelancer* function and then calls the *getInformationFromBidderProfile* function, passing in the profile URL, to retrieve all the relevant data from that profile.
It then adds the given profile to the profiles already seen, to prevent duplication within a single program execution.

getInformationFromBidderProfile
--------------------------------
.. code-block:: python

   getInformationFromBidderProfile(url)

This function retrieves all the relevant data from the profile of the given bidder, including qualifications. It makes calls to many helper functions, including *getCertifications* and *getReviewDetails*.
It takes 1 argument:

| - *url*: This is the url of the profile that is being looked at.

getCertifications
------------------
.. code-block:: python

   getCertifications()

This function retrieves all certifications from the 'Certifications' tab of the profile being looked at.

getReviewDetails
-----------------
.. code-block:: python

   getReviewDetails()

This function retrieves details about the reviews on the profile being currently looked at.

Saving to database
^^^^^^^^^^^^^^^^^^^

saveWinnerDetails
------------------------
.. code-block:: python

   saveWinnerDetails(jobID, url, user)

This function handles saving the details of project winners to the Winners table of the database.
It takes 3 arguments:

| - *jobID*: This is the unique code for the project that this bidder won and it is generated by Freelancer.

| - *url*: This is the URL for the project that this bidder won.

| - *user* This is the username of the bidder that was awarded this work.

saveQualificationDetails
--------------------------
.. code-block:: python

   saveQualificationDetails()

This function handles saving the details of qualifications of this user to the Qualifications table of the database.

saveReviewDetails
------------------
.. code-block:: python

   saveReviewDetails()

This function handles saving the details of a review of this user to the Reviews table of the database.

saveJobDetails
---------------
.. code-block:: python

   saveJobDetails(url)

This function handles saving the details of a project to the Jobs table of the database if the amount paid was not an hourly rate.
It takes 1 argument:

| - *url*: This is the URL for the project.

saveJobHourlyDetails
---------------------
.. code-block:: python

   saveJobHourlyDetails(url)

This function handles saving the details of a project to the JobsHourly table of the database if the amount paid was an hourly rate.
It takes 1 argument:

| - *url*: This is the URL for the project.

saveProfileDetails
-------------------
.. code-block:: python

   saveProfileDetails()

This function handles saving the details of a user's profile to the Profiles table of the database.

saveBidDetails
---------------
.. code-block:: python

   saveBidDetails(jobID, country, user)

This function handles saving the details of a bid to the Bids table of the database.
It takes 3 arguments:

| - *jobID*: This is the unique code for the project and it is generated by Freelancer.

| - *country*: The country of the user who bid for this project.

| - *user*: The username of the person who bid on this project

General helper functions
^^^^^^^^^^^^^^^^^^^^^^^^^
exit
-----
.. code-block:: python

   exit()

This function handles closing the program.

closeBrowser
-------------
.. code-block:: python

   closeBrowser()

This function closes the browser being used by the program, regardless of whether it is being run in headless mode.
The function then calls *exit* to close the program.

keyPressEvent
--------------
.. code-block:: python

   keyPressEvent(event)

This function overrides a function in the PyQt library and handles the user pressing keys during program execution.
This function only handles the use of the Enter key, which calls *setUpProgram*.