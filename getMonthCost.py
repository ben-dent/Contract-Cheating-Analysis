import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

yearMonths = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

data = []

count = [1, 1, 1, 1, 1, 1, 1, 259, 336, 329, 266, 265, 160, 170, 188, 222, 171, 147, 153, 164, 190, 232, 215, 199, 52, 75, 94, 105, 80, 63, 60, 57, 1, 1, 1, 1]
i = 0

for year in range(2017, 2020):
    for month in range(1, 13):
        total = 0
        num = 0
        monthName = yearMonths.get(month)
        cur.execute('SELECT SUM(ConvertedFinalCost) FROM Jobs WHERE Year = ' + str(year) + " AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()
        if r[0] is not None:
            num += r[0]

        cur.execute("SELECT SUM(ConvertedFinalCost) FROM ReviewJobs WHERE PossibleYears LIKE '%" + str(year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedFinalCost != 'None'")
        r = cur.fetchone()
        if r[0] is not None:
            num += r[0]

        # cur.execute("SELECT COUNT(ConvertedCurrency), SUM(ConvertedCurrency) FROM Reviews WHERE PossibleYears LIKE '%" + str(
        #     year) + "' AND PossibleMonths LIKE '%" + monthName + "%' AND ConvertedCurrency != 'None'")
        # r = cur.fetchone()
        # if r[0] is not None:
        #     num += r[0]
        #     total += 1

        data.append([str(year) + " - " + monthName + " - " + str(count[i]), '$' + '{0:,.2f}'.format(num), '$' + '{0:,.2f}'.format(num / count[i])])
        i += 1
    data.append("\n")



for each in data:
    print(str(each))