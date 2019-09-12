import sqlite3 as lite

import pandas as pd

con = lite.connect('JobDetails.db')
cur = con.cursor()

data = pd.read_csv('Attachments.txt', delimiter="\t")

for i in range(len(data.values)):
    print('Job ' + str(i + 1) + "/" + str(len(data.values)))
    vals = data.values[i]
    jID = vals[0]
    attach = vals[1]

    for table in ['Jobs', 'ReviewJobs']:
        query = 'UPDATE ' + table + ' SET Attachment = ' + str(attach) + ' WHERE JobID = ' + str(jID)
        cur.execute(query)
        con.commit()

