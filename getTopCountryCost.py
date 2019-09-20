import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

countries = ['United States', 'Australia', 'United Kingdom', 'United Arab Emirates', 'Singapore']

for i in range(len(countries)):
    country = countries[i]
    total = 0
    for table in ['Jobs', 'ReviewJobs']:
        query = "SELECT SUM(ConvertedFinalCost) FROM " + table + " WHERE CountryOfPoster = '" + country + "' AND ConvertedFinalCost != 'None'"
        cur.execute(query)
        r = cur.fetchone()

        if r[0] is not None:
            try:
                total += r[0]
            except TypeError:
                a = 1


    print(country + ": $" + '{0:,.2f}'.format(float(total)) + "\n")