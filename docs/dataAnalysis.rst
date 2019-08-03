Data Analysis.py
==============================

This file handles all the analysis of the data collected by the tool, as well as currency conversion to USD.

Its functions include generating graphs, saving to CSV files and converting currencies to USD, using historic conversion rates

Currency Conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This file contains numerous functions to handle currency conversion.

convertCurrency
-----------------
::

    convertCurrency(currency, amount, date)

This function takes in 3 parameters:

| - *currency*: This is the 3 character code for the currency from which the conversion is taking place

| - *amount*: This is a float that contains the amount of the currency to be converted