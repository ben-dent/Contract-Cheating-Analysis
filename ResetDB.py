import sqlite3 as lite

db = 'JobDetails.db'
con = lite.connect(db)
cur = con.cursor()

cur.execute('DROP TABLE Bids')
cur.execute('DROP TABLE Jobs')
cur.execute('DROP TABLE Profiles')
cur.execute('DROP TABLE Qualifications')
cur.execute('DROP TABLE Reviews')
cur.execute('DROP TABLE Winners')

con.commit()