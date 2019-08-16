import sqlite3 as lite

db = 'JobDetails.db'
con = lite.connect(db)
cur = con.cursor()

cur.execute("SELECT name from sqlite_master WHERE type='table'")

tables = [r[0] for r in cur.fetchall()]

for table in tables:
    query = 'DROP TABLE ' + table
    cur.execute(query)


# cur.execute('DROP TABLE Bids')
# cur.execute('DROP TABLE Jobs')
# cur.execute('DROP TABLE JobsHourly')
# cur.execute('DROP TABLE Profiles')
# cur.execute('DROP TABLE Qualifications')
# cur.execute('DROP TABLE Reviews')
# cur.execute('DROP TABLE Winners')

con.commit()