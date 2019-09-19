import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cur.execute("SELECT JobID, DateRange FROM ReviewJobs")
results = [list(each) for each in cur.fetchall()]

yearMonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

for result in results:
    jID = result[0]
    r = result[1]
    split = r.split('/')

    if len(r.split('-')) != 1:
        startMonth = int(split[1])
        endMonth = int(split[-2])
    else:
        startMonth = int(split[1])
        endMonth = startMonth

    months = yearMonths.get(startMonth)

    if startMonth != endMonth:
        months += ", "
        for i in range(int(startMonth) + 1, int(endMonth)):
            months += yearMonths.get(i) + ", "
        months += yearMonths.get(endMonth)

    cur.execute("UPDATE ReviewJobs SET PossibleMonths = '" + months + "' WHERE JobID = " + str(jID))

con.commit()