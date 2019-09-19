import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

profiles = ['Rachaelray', 'charleslimnet', 'basithashmi', 'citijayamala', 'janelleanne']

for i in range(len(profiles)):
    profile = profiles[i]
    query = "SELECT SUM(ConvertedCurrency) FROM Reviews WHERE Profile = '" + profile + "'"
    cur.execute(query)
    print(profile + ": $" + '{0:,.2f}'.format(float(cur.fetchone()[0])) + "\n")