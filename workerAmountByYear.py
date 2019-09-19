import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

amounts = {}

workers = ['Rachaelray', 'basithashmi', 'citijayamala', 'charleslimnet', 'janelleanne']

for year in range(2017, 2020):
    for i in range(len(workers)):
        worker = workers[i]
        print(str(year) + " - Worker " + str(i + 1) + "/5")
        cur.execute("SELECT SUM(ConvertedCurrency) FROM Reviews WHERE Profile = '" + worker + "' AND ConvertedCurrency != '' AND ConvertedCurrency != 'None' AND PossibleYears LIKE '%" + str(year) + "%'")
        num = cur.fetchone()[0]

        amounts.update({worker + " - " + str(year): num})

# topWorkers = [[reviews.get(number), number] for number in sorted(list(reviews.keys()))[-5:]]
# print(topWorkers)

print("\n######################\n")

for worker in list(amounts.keys()):
    print(worker + ":  $" + '{0:,.2f}'.format(amounts.get(worker)))
# bidNumbers = sorted(list(reviews.values()))[-5:]
#
# for user in reviews:
#     val = reviews.get(user)
#     if val in bidNumbers:
#         print(user + ": " + str(val) + " - $" + '{0:,.2f}'.format(amounts.get(user)))

