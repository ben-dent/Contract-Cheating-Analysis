Data Analysis.py
==============================

.. highlight:: python

This file handles all the analysis of the data collected by the tool, as well as currency conversion to USD.

Its functions include generating graphs, saving to CSV files and converting currencies to USD, using historic conversion rates

Currency Conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This file contains numerous functions to handle currency conversion.

convertCurrency
-----------------
::

    convertCurrency(currency, amount, date)

This function handles converting currency using the historic conversion rate of the given date. It takes in 3 parameters:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *date*: This is a ``date`` object from the ``datetime`` Python library that is the date to use for historic conversion

convertCurrencyWithYear
-------------------------
::

    convertCurrencyWithYear(currency, amount, week, year)

This function handles converting currency using the average rate for the given week in the given year. It takes in 4 parameters:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted

| - *week*: This is an integer that contains the week number of the given year to use for conversion

| - *year* This is an integer that contains the year to use for historic conversion
