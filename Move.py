import sqlite3 as lite

db1 = lite.connect('JobDetails.db')
cur1 = db1.cursor()

db2 = lite.connect('JobDetails-2.db')
cur2 = db2.cursor()

saved = []

for table in ['Jobs', 'ReviewJobs']:
    query = 'SELECT JobID FROM ' + table
    cur1.execute(query)
    saved += [each[0] for each in cur1.fetchall()]

toUse = []

for table in ['Jobs', 'ReviewJobs']:
    query = 'SELECT JobID FROM ' + table
    cur2.execute(query)
    toUse += [each[0] for each in cur2.fetchall() if each not in saved]

toAdd = []

for jID in toUse:
    for table in ['Jobs', 'ReviewJobs']:
        query = 'SELECT * FROM ' + table + ' WHERE JobID = ' + str(jID)
        cur2.execute(query)
        result = cur2.fetchone()
        if result is not None:
            res = [table, result]
            toAdd.append(res)

for data in toAdd:
    table = data[0]
    info = data[1]
    query = 'INSERT INTO ' + table + ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

    cur1.execute(query, info)