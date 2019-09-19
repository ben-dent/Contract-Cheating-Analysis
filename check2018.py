from datetimerange import DateTimeRange
from datetime import date
from dateutil.relativedelta import relativedelta
import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

finalResults = []

year = 2018

start = str(year) + "/1/1"
end = str(year) + "/12/31"

# start = date(year, 1, 1)
# end = date(year, 12, 31)

givenRange = DateTimeRange(start, end)

tables = ['Jobs', 'ReviewJobs']
columns = ['Year', 'PossibleYears']
data = []
# for i in range(len(tables)):
#     table = tables[i]
#     query = 'SELECT DateRange, ConvertedFinalCost FROM ' + table + " WHERE ConvertedFinalCost != 'None' AND " + columns[i] + " LIKE '%" + str(year) + "%'"
#     cur.execute(query)
#     results = [list(each) for each in cur.fetchall()]
#
#     for j in range(len(results)):
#         job = results[j]
#         data.append(float(job[1]))
#
# totalMade = sum(data)
# toAppend = str(year) + ": " + '${0:,.2f}'.format(totalMade) + " - Average of " + '${0:,.2f}'.format(totalMade / len(data)) + " Across " + str(len(data))
# finalResults.append(toAppend)
#
# print("\n###################\n")
# print(str(finalResults) + "\n\n#################\n\n")
#
# data = []
# finalResults = []
#
# seen = 0
#
# for i in range(len(tables)):
#     table = tables[i]
#     query = 'SELECT DateRange, ConvertedFinalCost FROM ' + table + " WHERE ConvertedFinalCost != 'None' AND " + columns[i] + " LIKE '%" + str(year) + "%'"
#     cur.execute(query)
#     results = [list(each) for each in cur.fetchall()]
#
#     for j in range(len(results)):
#         job = results[j]
#         data.append(float(job[1]))
#
#         dateRange = job[0]
#         d = [each.lstrip().rstrip() for each in dateRange.split("-")]
#
#         s = d[0].split("/")
#         startFormat = str(int(s[2]) + 2000) + "/" + s[1] + "/" + s[0]
#
#         inRange = False
#
#         if len(d) > 1:
#             e = d[1].split("/")
#             endFormat = str(int(e[2]) + 2000) + "/" + e[1] + "/" + e[0]
#
#             tableRange = DateTimeRange(startFormat, endFormat)
#
#             for day in tableRange.range(relativedelta(days=1)):
#                 if day in givenRange:
#                     inRange = True
#
#         else:
#             inRange = startFormat in givenRange
#
#         if inRange:
#             seen += 1
#             data.append(float(job[1]))
#
# totalMade = sum(data)
# toAppend = str(year) + ": " + '${0:,.2f}'.format(totalMade) + " - Average of " + '${0:,.2f}'.format(totalMade / len(data)) + " Across " + str(len(data))
# finalResults.append(toAppend)
#
# print("\n###################\n" + str(seen) + "\n")
# print(str(finalResults) + "#################")

query = "SELECT DateRange, ConvertedFinalCost FROM ReviewJobs WHERE ConvertedFinalCost != 'None' AND PossibleYears LIKE '%2018%'"
cur.execute(query)
results = [list(each) for each in cur.fetchall()]

for j in range(len(results)):
    job = results[j]
    data.append(float(job[1]))

query = "SELECT DateRange, ConvertedFinalCost FROM Jobs WHERE ConvertedFinalCost != 'None' AND Year = 2018"
cur.execute(query)
results = [list(each) for each in cur.fetchall()]

for j in range(len(results)):
    job = results[j]
    data.append(float(job[1]))

totalMade = sum(data)
toAppend = str(year) + ": " + '${0:,.2f}'.format(totalMade) + " - Average of " + '${0:,.2f}'.format(totalMade / len(data)) + " Across " + str(len(data))
finalResults.append(toAppend)

print("\n###################\n")
print(str(finalResults) + "\n\n#################\n\n")

data = []
finalResults = []

seen = 0

query = "SELECT DateRange, ConvertedFinalCost FROM ReviewJobs WHERE ConvertedFinalCost != 'None' AND PossibleYears LIKE '%2018%'"
cur.execute(query)
results = [list(each) for each in cur.fetchall()]
for j in range(len(results)):
    job = results[j]
    data.append(float(job[1]))

    dateRange = job[0]
    d = [each.lstrip().rstrip() for each in dateRange.split("-")]

    s = d[0].split("/")
    startFormat = str(int(s[2]) + 2000) + "/" + s[1] + "/" + s[0]

    inRange = False

    if len(d) > 1:
        e = d[1].split("/")
        endFormat = str(int(e[2]) + 2000) + "/" + e[1] + "/" + e[0]

        tableRange = DateTimeRange(startFormat, endFormat)

        for day in tableRange.range(relativedelta(days=1)):
            if day in givenRange:
                inRange = True

    else:
        inRange = startFormat in givenRange

    if inRange:
        seen += 1
        data.append(float(job[1]))

query = "SELECT DateRange, ConvertedFinalCost FROM Jobs WHERE ConvertedFinalCost != 'None' AND Year = 2018"
cur.execute(query)
results = [list(each) for each in cur.fetchall()]
for j in range(len(results)):
    job = results[j]
    data.append(float(job[1]))

    dateRange = job[0]
    d = [each.lstrip().rstrip() for each in dateRange.split("-")]

    s = d[0].split("/")
    startFormat = str(int(s[2]) + 2000) + "/" + s[1] + "/" + s[0]

    inRange = False

    if len(d) > 1:
        e = d[1].split("/")
        endFormat = str(int(e[2]) + 2000) + "/" + e[1] + "/" + e[0]

        tableRange = DateTimeRange(startFormat, endFormat)

        for day in tableRange.range(relativedelta(days=1)):
            if day in givenRange:
                inRange = True

    else:
        inRange = startFormat in givenRange

    if inRange:
        seen += 1
        data.append(float(job[1]))

totalMade = sum(data)
toAppend = str(year) + ": " + '${0:,.2f}'.format(totalMade) + " - Average of " + '${0:,.2f}'.format(totalMade / len(data)) + " Across " + str(len(data))
finalResults.append(toAppend)

print("\n###################\n" + str(seen) + "\n")
print(str(finalResults) + "#################")