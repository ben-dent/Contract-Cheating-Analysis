import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cs = {}
amounts = {}

# for table in ['Reviews']:
#     cur.execute("SELECT Country FROM " + table)
#     countries = [each[0] for each in cur.fetchall()]
countries = []

for table in ['Jobs', 'ReviewJobs']:
    cur.execute("SELECT CountryOfPoster FROM " + table)
    countries += [each[0] for each in cur.fetchall()]

# for i in range(len(countries)):
#     country = countries[i]
#     num = cs.get(country)
#     if num is None:
#         cs.update({country: 1})
#     else:
#         cs.update({country: num + 1})


# cur.execute("SELECT Country, ConvertedCurrency FROM Reviews WHERE ConvertedCurrency != '' AND ConvertedCurrency != 'None' AND ConvertedCurrency != 'Unavailable'")
# results = [list(each) for each in cur.fetchall()]
#
# for result in results:
#     country = result[0]
#     paid = float(result[1])
#     num = amounts.get(country)
#     if num is None:
#         amounts.update({country: paid})
#     else:
#         amounts.update({country: num + paid})

cur.execute("SELECT CountryOfPoster, ConvertedFinalCost FROM Jobs WHERE ConvertedFinalCost != '' AND ConvertedFinalCost != 'None' AND ConvertedFinalCost != 'Unavailable'")
results = [list(each) for each in cur.fetchall()]

print(len(results))

for result in results:
    country = result[0]
    paid = float(result[1])
    num = amounts.get(country)
    if num is None:
        amounts.update({country: paid})
    else:
        amounts.update({country: num + paid})

    num = cs.get(country)
    if num is None:
        cs.update({country: 1})
    else:
        cs.update({country: num + 1})


cur.execute("SELECT CountryOfPoster, ConvertedFinalCost FROM ReviewJobs WHERE ConvertedFinalCost != '' AND ConvertedFinalCost != 'None' AND ConvertedFinalCost != 'Unavailable'")
results = [list(each) for each in cur.fetchall()]
print(len(results))

for result in results:
    country = result[0]
    paid = float(result[1])
    num = amounts.get(country)
    if num is None:
        amounts.update({country: paid})
    else:
        amounts.update({country: num + paid})

    num = cs.get(country)
    if num is None:
        cs.update({country: 1})
    else:
        cs.update({country: num + 1})

countryNums = sorted(list(cs.values()))[-5:]

uniqueCs = list(cs.keys())

topCountries = []

theCountries = []

for i in range(len(uniqueCs)):
    country = uniqueCs[i]
    print("Country " + str(i + 1) + "/" + str(len(cs.keys())))

    if cs.get(country) in countryNums:
        topCountries.append([country + ": " + str(cs.get(country))])
        theCountries.append(country)

print("\n\nCountries: " + str(topCountries) + "\n\n")

for country in theCountries:
    print(country + ": " + '${0:,.2f}'.format(amounts.get(country)) + ' - Average: $' + '{0:,.2f}'.format(amounts.get(country) / cs.get(country)))