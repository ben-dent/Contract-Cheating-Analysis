import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

jIDs = []

bids = {}
cs = {}

bidders = []

countries = []

for table in ['Jobs', 'ReviewJobs']:
    cur.execute("SELECT JobID FROM " + table + " WHERE ((Category = 4) OR (Category = 5))")
    jIDs += [each[0] for each in cur.fetchall()]

for i in range(len(jIDs)):
    job = jIDs[i]
    print("Job " + str(i + 1) + "/" + str(len(jIDs)))
    cur.execute("SELECT User, Country FROM Bids WHERE JobID = " + str(job))
    result = cur.fetchall()

    for each in result:
        bidders.append(each[0])
        countries.append(each[1])

numBids = len(bidders)

for i in range(len(bidders)):
    bidder = bidders[i]
    print("Bidder " + str(i + 1) + "/" + str(len(bidders)))
    num = bids.get(bidder)
    if num is None:
        bids.update({bidder: 1})
    else:
        bids.update({bidder: num + 1})

for i in range(len(countries)):
    country = countries[i]
    print("Country " + str(i + 1) + "/" + str(len(countries)))
    num = cs.get(country)
    if num is None:
        cs.update({country: 1})
    else:
        cs.update({country: num + 1})


nums = sorted(list(bids.values()))[-5:]

uniqueBs = list(bids.keys())

topBidders = []

for i in range(len(uniqueBs)):
    bidder = uniqueBs[i]
    print("Bidder " + str(i + 1) + "/" + str(len(bidders)))

    if bids.get(bidder) in nums:
        topBidders.append([bidder + ": " + str(bids.get(bidder))])

# topBidders = [[bids.get(number), number] for number in sorted(list(bids.keys()))[-5:]]

countryNums = sorted(list(cs.values()))[-5:]

uniqueCs = list(cs.keys())

topCountries = []

for i in range(len(uniqueCs)):
    country = uniqueCs[i]
    print("Country " + str(i + 1) + "/" + str(len(countries)))

    if cs.get(country) in countryNums:
        topCountries.append([country + ": " + str(cs.get(country))])

# topCountries = [[cs.get(number), number] for number in sorted(list(cs.keys()))[-5:]]


print("Bidders: " + str(topBidders))
print("Countries: " + str(topCountries))

a = 1