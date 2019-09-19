import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

reviews = {}

cur.execute('SELECT DISTINCT(Profile) FROM Reviews')
workers = [each[0] for each in cur.fetchall()]

for i in range(len(workers)):
    bidder = workers[i]
    print("Worker " + str(i + 1) + "/" + str(len(workers)))
    cur.execute("SELECT COUNT(ReviewID) FROM Reviews WHERE Profile = '" + bidder + "'")
    reviews.update({bidder: cur.fetchone()[0]})

# topWorkers = [[reviews.get(number), number] for number in sorted(list(reviews.keys()))[-5:]]
# print(topWorkers)

cur.execute('SELECT DISTINCT(Profile) FROM ReviewJobs WHERE URL NOT IN (SELECT ProjectURL FROM Reviews)')
workers = [each[0] for each in cur.fetchall()]

for i in range(len(workers)):
    bidder = workers[i]
    print("Worker " + str(i + 1) + "/" + str(len(workers)))
    cur.execute("SELECT COUNT(Profile) FROM ReviewJobs WHERE Profile = '" + bidder + "'")
    reviews.update({bidder: cur.fetchone()[0]})


print("\n######################\n")
bidNumbers = sorted(list(reviews.values()))[-5:]

for user in reviews:
    val = reviews.get(user)
    if val in bidNumbers:
        print(user + ": " + str(val))