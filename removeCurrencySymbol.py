import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cur.execute("SELECT BidID, Price FROM Bids")
results = [list(each) for each in cur.fetchall()]

for i in range(len(results)):
    result = results[i]
    print("Bid " + str(i + 1) + "/" + str(len(results)))
    bID = str(result[0])
    price = ''.join(c for c in result[1] if c.isnumeric() or c == '.')

    query = "UPDATE Bids SET Price = '" + price + "' WHERE BidID = " + bID
    cur.execute(query)

con.commit()