import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

reviews = {}
amounts = {}

cur.execute('SELECT DISTINCT(Profile) FROM Reviews')
workers = [each[0] for each in cur.fetchall()]

for i in range(len(workers)):
    bidder = workers[i]
    print("Worker " + str(i + 1) + "/" + str(len(workers)))
    cur.execute("SELECT COUNT(ReviewID), SUM(ConvertedCurrency) FROM Reviews WHERE Profile = '" + bidder + "'")
    r = cur.fetchone()
    reviews.update({bidder: r[0]})
    amounts.update(({bidder: r[1]}))

# topWorkers = [[reviews.get(number), number] for number in sorted(list(reviews.keys()))[-5:]]
# print(topWorkers)

print("\n######################\n")
bidNumbers = sorted(list(reviews.values()))[-5:]

for user in reviews:
    val = reviews.get(user)
    if val in bidNumbers:
        print(user + ": " + str(val) + " - $" + '{0:,.2f}'.format(amounts.get(user)))