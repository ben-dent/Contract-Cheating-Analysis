import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()


def doScore():
    for table in ['Jobs', 'ReviewJobs']:
        query = "SELECT JobID, Category FROM " + table + " WHERE CategoryTypeTwo IS NULL"
        cur.execute(query)
        results = cur.fetchall()

        for result in results:
            jID = result[0]
            cat = result[1]
            if (cat == 4) or (cat == 5):
                category = 3
            elif (cat == 3):
                category = 2
            else:
                category = 1

            query = "UPDATE " + table + " SET CategoryTypeTwo = " + str(category) + " WHERE JobID = " + str(jID)
            cur.execute(query)
        con.commit()

