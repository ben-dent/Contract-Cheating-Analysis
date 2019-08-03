Crawler.py
================

This is a Python file that carries out the web crawling in the program.

It contains one constant and one function:

LINK_PREFIX
^^^^^^^^^^^^^^^
::

    LINK_PREFIX = "https://www.freelancer.co.uk"

This constant is used to avoid having to type out the same url multiple times.

getAllTheRelevantLinks
^^^^^^^^^^^^^^^^^^^^^^
::

    getAllTheRelevantLinks(url)

This function takes a single parameter, the URL of a week in the project archive of the Freelancer site.