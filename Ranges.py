import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

highs = {}
lows = {}

for i in range(1, 6):
    query = "SELECT Score FROM Jobs WHERE Category = " + str(i)
    cur.execute(query)


    results = [r[0] for r in cur.fetchall()]
    output = "For Job Category " + str(i) + " - "

    if len(results) == 0:
        output += "No results"
    else:
        output += "Max of: " + str(max(results)) + " and Min of: " + str(min(results))

    print(output + "\n")

    query = "SELECT Score FROM ReviewJobs WHERE Category = " + str(i)
    cur.execute(query)

    results = [r[0] for r in cur.fetchall()]
    output = "For Review Job Category " + str(i) + " - "

    if len(results) == 0:
        output += "No results"
    else:
        output += "Max of: " + str(max(results)) + " and Min of: " + str(min(results))

    print(output + "\n")
