import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

bids = {}

cur.execute('SELECT DISTINCT(User) FROM Bids')
bidders = [each[0] for each in cur.fetchall()]

for i in range(len(bidders)):
    bidder = bidders[i]
    print("Bidder " + str(i + 1) + "/" + str(len(bidders)))
    cur.execute("SELECT COUNT(BidID) FROM Bids WHERE User = '" + bidder + "'")
    bids.update({bidder: cur.fetchone()[0]})
    # bids.update({cur.fetchone()[0]: bidder})

print("\n######################\n")
sortedList = sorted(list(bids.values()))
bidNumbers = sortedList[-5:]

for bidder in bidders:
    val = bids.get(bidder)
    if val in bidNumbers:
        print(bidder + ": " + str(val))

# topBidders = [[bids.get(number), number] for number in sorted(list(bids.keys()))[-5:]]