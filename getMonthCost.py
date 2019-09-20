import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

yearMonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

data = []

for year in range(2017, 2020):
    for month in range(1, 13):
        total = 0
        num = 0
        monthName = yearMonths.get(month)
        cur.execute('SELECT COUNT(ConvertedFinalCost), SUM(ConvertedFinalCost) FROM Jobs WHERE Year = ' + str(year) + " AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()
        if r[0] is not None:
            num += r[0]
            total += 1

        cur.execute("SELECT COUNT(ConvertedFinalCost), SUM(ConvertedFinalCost) FROM ReviewJobs WHERE PossibleYears LIKE '%" + str(year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()
        if r[0] is not None:
            num += r[0]
            total += 1

        cur.execute("SELECT COUNT(ConvertedCurrency), SUM(ConvertedCurrency) FROM Reviews WHERE PossibleYears LIKE '%" + str(
            year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedCurrency != 'None'")
        r = cur.fetchone()
        if r[0] is not None:
            num += r[0]
            total += 1

        data.append([str(year) + " - " + monthName, '$' + '{0:,.2f}'.format(num), '$' + '{0:,.2f}'.format(num / total)])
    data.append("\n")


for each in data:
    print(str(each))