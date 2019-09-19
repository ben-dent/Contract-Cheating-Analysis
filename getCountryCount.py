import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

data = {}

cur.execute("SELECT DISTINCT(CountryOfWinner) FROM Jobs WHERE CountryOfWinner !='None'")

countries = [each[0] for each in cur.fetchall()]

cur.execute("SELECT DISTINCT(CountryOfWinner) FROM ReviewJobs WHERE CountryOfWinner !='None'")

countries += [each[0] for each in cur.fetchall() if each[0] not in countries]

for i in range(len(countries)):
    country = countries[i]
    print("Country " + str(i + 1) + "/" + str(len(countries)))

    cur.execute("SELECT COUNT(CountryOfWinner) FROM Jobs WHERE CountryOfWinner = '" + country + "'")
    num = cur.fetchone()[0]

    cur.execute("SELECT COUNT(CountryOfWinner) FROM ReviewJobs WHERE CountryOfWinner = '" + country + "'")
    num += cur.fetchone()[0]

    data.update({num: country})

topCountries = [[data.get(number), number] for number in sorted(list(data.keys()))[-5:]]

print(topCountries)