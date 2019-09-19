import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

yearMonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

data = []

for year in range(2013, 2020):
    for month in range(1, 13):
        num = 0
        monthName = yearMonths.get(month)
        cur.execute('SELECT SUM(ConvertedFinalCost) FROM Jobs WHERE Year = ' + str(year) + " AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()[0]
        if r is not None:
            num += r

        cur.execute("SELECT SUM(ConvertedFinalCost) FROM ReviewJobs WHERE PossibleYears LIKE '%" + str(year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()[0]
        if r is not None:
            num += r

        cur.execute("SELECT SUM(ConvertedCurrency) FROM Reviews WHERE PossibleYears LIKE '%" + str(
            year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedCurrency != 'None'")
        r = cur.fetchone()[0]
        if r is not None:
            num += r

        data.append([str(year) + " - " + monthName, '$' + '{0:,.2f}'.format(num)])
    data.append("\n")


for each in data:
    print(str(each))