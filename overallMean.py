import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cur.execute("SELECT SUM(ConvertedCurrency), COUNT(ConvertedCurrency) FROM Reviews")
results = cur.fetchone()
sum = results[0]
num = results[1]

for table in ['Jobs', 'ReviewJobs']:
    cur.execute("SELECT ConvertedFinalCost FROM " + table + " WHERE ConvertedFinalCost != 'None' AND URL NOT IN (SELECT ProjectURL FROM Reviews)")
    results = [float(each[0]) for each in cur.fetchall()]

    for amount in results:
        sum += amount
        num += 1


print("Total: $" + '{0:,.2f}'.format(sum))
print("Number: " + str(num))
print("Average: $" + '{0:,.2f}'.format((sum / num)))

