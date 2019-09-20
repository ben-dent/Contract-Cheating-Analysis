import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cur.execute("SELECT JobID, ConvertedFinalCost FROM ReviewJobs")
results = [list(each) for each in cur.fetchall()]

for i in range(len(results)):
    result = results[i]
    print("Job " + str(i + 1) + "/" + str(len(results)))
    bID = str(result[0])
    price = ''.join(c for c in str(result[1]) if c.isnumeric() or c == '.')

    query = "UPDATE ReviewJobs SET ConvertedFinalCost = '" + price + "' WHERE JobID = " + bID
    cur.execute(query)

con.commit()