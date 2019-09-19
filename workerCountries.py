import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

cs = {}

cur.execute('SELECT DISTINCT(User) FROM Bids')
users = [each[0] for each in cur.fetchall()]

# cur.execute('SELECT DISTINCT(Profile) FROM Reviews')
# profiles = [each[0] for each in cur.fetchall() if each[0] not in users]

for i in range(len(users)):
    user = users[i]
    print("User " + str(i + 1) + "/" + str(len(users)))

    cur.execute("SELECT Country FROM Bids WHERE User = '" + user + "'")
    countries = [each[0] for each in cur.fetchall()]
    for country in countries:
        num = cs.get(country)
        if num is None:
            cs.update({country: 1})
        else:
            cs.update({country: num + 1})

# for i in range(len(profiles)):
#     profile = profiles[i]
#     print("Profile " + str(i + 1) + "/" + str(len(profiles)))
#
#     cur.execute("SELECT Country FROM Profiles WHERE Username = '" + profile + "'")
#     countries = [each[0] for each in cur.fetchall()]
#     for country in countries:
#         num = cs.get(country)
#         if num is None:
#             cs.update({country: 1})
#         else:
#             cs.update({country: num + 1})


countryNums = sorted(list(cs.values()))[-5:]

uniqueCs = list(cs.keys())

topCountries = []

for i in range(len(uniqueCs)):
    country = uniqueCs[i]
    print("Country " + str(i + 1) + "/" + str(len(cs.keys())))

    if cs.get(country) in countryNums:
        topCountries.append([country + ": " + str(cs.get(country))])


print("Countries: " + str(topCountries))