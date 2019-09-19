import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

oldest = 9999

cols = {'Reviews': 'PossibleYears', 'ReviewJobs': 'PossibleYears', 'Jobs': 'Year'}

for table in ['Reviews', 'Jobs', 'ReviewJobs']:
    cur.execute("SELECT " + cols.get(table) + " FROM " + table)
    results = [each[0] for each in cur.fetchall()]

    for year in results:
        split = [each.lstrip().rstrip() for each in str(year).split(',')]
        for item in split:
            if int(item) < oldest:
                oldest = int(item)

print(str(oldest))
