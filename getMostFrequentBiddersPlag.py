import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

bids = {}

jIDs = []

numBidders = 0

for table in ['Jobs', 'ReviewJobs']:
    cur.execute('SELECT JobID FROM ' + table + ' WHERE Category = 4 OR Category = 5')
    jIDs += [each[0] for each in cur.fetchall()]

for jID in jIDs:
    cur.execute('SELECT COUNT(User) FROM Bids WHERE JobID = ' + str(jID))
    numBidders += cur.fetchone()[0]

    # for i in range(len(bidders)):
    #     bidder = bidders[i]
    #     print("Bidder " + str(i + 1) + "/" + str(len(bidders)))
    #     cur.execute("SELECT COUNT(BidID) FROM Bids WHERE User = '" + bidder + "'")
    #     bids.update({bidder: cur.fetchone()[0]})
    #     # bids.update({cur.fetchone()[0]: bidder})

print("Number of jobs: " + str(len(jIDs)))
print("Number of bids: " + str(numBidders))
print("Average number of bids: " + str(numBidders / len(jIDs)))

# print("\n######################\n")
# sortedList = sorted(list(bids.values()))
# bidNumbers = sortedList[-5:]

# for bidder in bidders:
#     val = bids.get(bidder)
#     if val in bidNumbers:
#         print(bidder + ": " + str(val))

# topBidders = [[bids.get(number), number] for number in sorted(list(bids.keys()))[-5:]]