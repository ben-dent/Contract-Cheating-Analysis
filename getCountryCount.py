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
    s = 0
    num = 0

    cur.execute("SELECT COUNT(CountryOfWinner), SUM(ConvertedFinalCost) FROM Jobs WHERE CountryOfWinner = '" + country + "' AND ConvertedFinalCost != '' AND ConvertedFinalCost != 'None' AND ConvertedFinalCost != 'Unavailable' AND ((Category = 4) OR (Category = 5))")
    r = cur.fetchone()
    if r[1] is not None:
        num += r[0]
        s += r[1]
    else:
        a = 1

    cur.execute("SELECT COUNT(CountryOfWinner), SUM(ConvertedFinalCost), ConvertedFinalCost FROM ReviewJobs WHERE CountryOfWinner = '" + country + "' AND ConvertedFinalCost != '' AND ConvertedFinalCost != 'None' AND ConvertedFinalCost != 'Unavailable' AND ((Category = 4) OR (Category = 5))")
    r = cur.fetchone()
    if r[1] is not None:
        num += r[0]
        s += r[1]

    if num != 0:
        data.update({num: country + " - " + '${0:,.2f}'.format(s) + " - Average of " + '${0:,.2f}'.format(s / num)})

topCountries = [[data.get(number), number] for number in sorted(list(data.keys()))[-5:]]

print(topCountries)