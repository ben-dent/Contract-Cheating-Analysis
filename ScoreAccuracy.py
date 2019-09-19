import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

queries = [
    'SELECT COUNT(JobID) FROM Jobs WHERE ((Score != 5) AND (Score != 4)) AND ((Category = 4) OR (Category = 5))',
    'SELECT COUNT(JobID) FROM ReviewJobs WHERE ((Score != 5) AND (Score != 4)) AND ((Category = 4) OR (Category = 5))',
    'SELECT COUNT(JobID) FROM Jobs WHERE ((Score = 5) OR (Score = 4)) AND ((Category != 4) AND (Category != 5))',
    'SELECT COUNT(JobID) FROM ReviewJobs WHERE ((Score = 5) OR (Score = 4)) AND ((Category != 4) AND (Category != 5))'
]

numWrong = 0

for query in queries:
    cur.execute(query)
    numWrong += cur.fetchone()[0]

numCategorised = 0

for table in ['Jobs', 'ReviewJobs']:
    query = "SELECT COUNT(JobID) FROM " + table +  " WHERE Category IS NOT NULL AND Category != 'None'"
    cur.execute(query)
    numCategorised += cur.fetchone()[0]

correct = numCategorised - numWrong
pctCorrect = round((correct / numCategorised), 2) * 100

print('Correct: ' + str(correct) + "/" + str(numCategorised) + " (" + str(pctCorrect) + "%)")

diffs = 0

for table in ['Jobs', 'ReviewJobs']:
    query = 'SELECT SUM(ABS(Score - Category)) FROM ' + table + " WHERE Category IS NOT NULL AND Category != 'None'"
    cur.execute(query)
    diffs += cur.fetchone()[0]

print('Average Difference: ' + str(diffs / numCategorised))

fiveScore = 0

for table in ['Jobs', 'ReviewJobs']:
    cur.execute('SELECT COUNT(JobID) FROM ' + table + " WHERE Category = 5")
    numFives = cur.fetchone()[0]

for table in ['Jobs', 'ReviewJobs']:
    query = "SELECT COUNT(JobID) FROM " + table +  " WHERE (Category = 5 AND Score = 5)"
    cur.execute(query)
    fiveScore += cur.fetchone()[0]

pctCorrect = round((fiveScore / numFives), 2) * 100

print('Correct: ' + str(fiveScore) + "/" + str(numFives) + " (" + str(pctCorrect) + "%)")