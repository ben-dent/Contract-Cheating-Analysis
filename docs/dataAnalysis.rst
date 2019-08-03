Data Analysis.py
===============================

This file handles all the analysis of the data collected by the tool, as well as currency conversion to USD.

Its functions include generating graphs, saving to CSV files and converting currencies to USD, using historic conversion rates

Currency Conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This file contains numerous functions to handle currency conversion.

*convertCurrency*
-----------------
.. code-block:: python

    convertCurrency(currency, amount, date)

This function handles converting currency using the historic conversion rate of the given date.
It takes 3 arguments:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *date*: This is a ``date`` object from the ``datetime`` Python library that is the date to use for historic conversion

*convertCurrencyWithYear*
-------------------------
.. code-block:: python

    convertCurrencyWithYear(currency, amount, week, year)

This function handles converting currency using the average rate for the given week in the given year.
It takes 4 arguments:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *week*: This is an integer that contains the week number of the given year to use for conversion

| - *year* This is an integer that contains the year to use for historic conversion

*dateRange*
----------
.. code-block:: python

   daterange(startDate, endDate)

This function returns an iterable object with all the dates between *startDate* and *endDate*
It takes 2 arguments:

| - *startDate*: This is a ``date`` object from the ``datetime`` Python library that is the start date to use for the range

| - *endDate*: This is a ``date`` object from the ``datetime`` Python library that is the end date to use for the range


*getAverage*
-----------
.. code-block:: python

   getAverage(currency, startDate, endDate, amount)

This function handles converting currency by calculating the average conversion rate for the time period and using that to calculate a value in USD.
It takes 4 arguments

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *startDate*: This is a ``date`` object from the ``datetime`` Python library that is the start date to use for calculating the average

| - *endDate*: This is a ``date`` object from the ``datetime`` Python library that is the end date to use for calculating the average

| - *amount*: This is a float that contains the amount of the currency to be converted

*calculateWeeklyAverage*
------------------------
.. code-block:: python

   calculateWeeklyAverage(currency, amount, weeksAgo)

This function will calculate the average exchange rate for a given week and use that to perform a conversion to USD.
It takes 3 arguments:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *weeksAgo* This is an integer that contains the number of weeks since the desired week

*calculateMonthlyAverage*
------------------------
.. code-block:: python

   calculateWeeklyAverage(currency, amount, monthsAgo)

This function will calculate the average exchange rate for a given month and use that to perform a conversion to USD.
It takes 3 arguments:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *monthsAgo* This is an integer that contains the number of months since the desired month

*calculateYearlyAverage*
------------------------
.. code-block:: python

   calculateWeeklyAverage(currency, amount, year)

This function will calculate the average exchange rate for a given month and use that to perform a conversion to USD.
It takes 3 arguments:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *year* This is an integer that contains the desired year for which to get an average

Analysis
^^^^^^^^^
*plotBarChartsOfBidderCountries*
-------------------------------
.. code-block:: python

   plotBarChartsOfBidderCountries(countryValues)

This function produces multiple bar charts to show the number of bidders from each country.
It takes 1 argument:

| - *countryValues*: This is a dictionary of country names (Strings) to integers containing the number of bidders from that country. It also produces graphs by continent.


*plotFromDatabase*
-----------------

.. code-block:: python

   plotFromDatabase()

This function reads in data from the program database and will produce graphs from it by calling *plotBarChartsOfBidderCountries*

*saveDataToCSV*
--------------
.. code-block:: python

   saveDataToCSV(data)

This function handles saving data to CSV files for easy analysis in programs such as Microsoft Excel.
It takes 1 argument:

| - *data*: This is a list of the data to be saved to a CSV file