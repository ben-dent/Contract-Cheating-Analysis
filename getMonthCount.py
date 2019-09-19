import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

yearMonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

data = []

for year in range(2017, 2020):
    for month in range(1, 13):
        monthName = yearMonths.get(month)
        cur.execute('SELECT COUNT(JobID) FROM Jobs WHERE Year = ' + str(year) + " AND PossibleMonths LIKE '%" + monthName + "%'")
        num = cur.fetchone()[0]

        cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE PossibleYears LIKE '%" + str(year) + "' AND PossibleMonths LIKE '%" + monthName + "%'")
        num += cur.fetchone()[0]

        cur.execute("SELECT COUNT(ReviewID) FROM Reviews WHERE PossibleYears LIKE '%" + str(
            year) + "' AND PossibleMonths LIKE '%" + monthName + "%'")
        num += cur.fetchone()[0]

        data.append([str(year) + " - " + monthName, num])
    data.append("\n")


for each in data:
    print(str(each))