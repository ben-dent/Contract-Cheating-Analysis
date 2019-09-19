import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

biggest = 0
jID = 0

cur.execute("SELECT ReviewID, ConvertedCurrency FROM Reviews WHERE ConvertedCurrency != ''")
results = [list(each) for each in cur.fetchall()]

for result in results:
    if float(result[1]) > biggest:
        biggest = float(result[1])
        jID = result[0]

print("Reviews")
print('${0:,.2f}'.format(biggest))
print(str(jID) + "\n\n##########\n\n")

biggest = 0
jID = 0

cur.execute("SELECT JobID, ConvertedFinalCost FROM Jobs WHERE ConvertedFinalCost != '' and ConvertedFinalCost != 'None'")
results = [list(each) for each in cur.fetchall()]

for result in results:
    if float(result[1]) > biggest:
        biggest = float(result[1])
        jID = result[0]

print("Jobs")
print('${0:,.2f}'.format(biggest))
print(str(jID) + "\n\n##########\n\n")

biggest = 0
jID = 0

cur.execute("SELECT JobID, ConvertedFinalCost FROM ReviewJobs WHERE ConvertedFinalCost != '' and ConvertedFinalCost != 'None'")
results = [list(each) for each in cur.fetchall()]

for result in results:
    if float(result[1]) > biggest:
        biggest = float(result[1])
        jID = result[0]

print("Review Jobs")
print('${0:,.2f}'.format(biggest))
print(str(jID) + "\n\n##########\n\n")