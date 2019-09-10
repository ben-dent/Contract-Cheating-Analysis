import sqlite3 as lite

db1 = lite.connect('JobDetails.db')
cur1 = db1.cursor()

db2 = lite.connect('JobDetails-2.db')
cur2 = db2.cursor()

saved = []

cur1.execute('SELECT ProjectURL FROM Reviews')
saved = [each[0] for each in cur1.fetchall()]

toUse = []

cur2.execute('SELECT ProjectURL FROM Reviews')
toUse = [each[0] for each in cur2.fetchall() if each[0] not in saved]

for url in toUse:
    query = "SELECT * FROM Reviews WHERE ProjectURL = '" + url + "'"
    cur2.execute(query)
    result = cur2.fetchone()[1:]
    cur1.execute('INSERT INTO Reviews(ProjectURL, Tags, Profile, Score, AmountPaid, Currency, ConvertedCurrency, DateScraped, Date, Country, Notes, DateRange) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                 result)

db1.commit()

# saved = []

# for table in ['Jobs', 'ReviewJobs']:
#     query = 'SELECT JobID FROM ' + table
#     cur1.execute(query)
#     saved += [each[0] for each in cur1.fetchall()]
#
# toUse = []
#
# for table in ['Jobs', 'ReviewJobs']:
#     query = 'SELECT JobID FROM ' + table
#     cur2.execute(query)
#     toUse += [each[0] for each in cur2.fetchall() if each[0] not in saved]
#
# x = 0
# for i in toUse:
#     if i in saved:
#         x += 1
#
# b = 2
#
# toAdd = []
#
# for jID in toUse:
#     for table in ['Jobs', 'ReviewJobs']:
#         query = 'SELECT * FROM ' + table + ' WHERE JobID = ' + str(jID)
#         cur2.execute(query)
#         result = cur2.fetchone()
#         if result is not None:
#             res = [table, result + (0,)]
#             toAdd.append(res)
#
# for data in toAdd:
#     table = data[0]
#     info = data[1]
#     query = 'INSERT INTO ' + table + ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
#
#     cur1.execute(query, info)
#
# db1.commit()