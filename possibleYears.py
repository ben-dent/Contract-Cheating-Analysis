import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cur.execute("SELECT ReviewID, DateRange FROM Reviews")

results = cur.fetchall()

for result in results:
    rID = result[0]
    r = result[1]

    split = r.split("-")
    slash = r.split("/")

    if len(split) == 1:
        years = str(2000 + int(slash[-1]))
    else:
        years = ""

        for i in range(2000 + int(split[0].split("/")[-1]), 2000 + int(split[-2].split("/")[-1])):
            years += str(i) + ", "

        years += str(2000 + int(split[-1].split("/")[-1]))

    cur.execute("UPDATE Reviews SET PossibleYears = '" + years + "' WHERE ReviewID = " + str(rID))

con.commit()

