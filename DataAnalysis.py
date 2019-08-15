# import matplotlib.pyplot as plt; plt.rcdefaults()
import csv
import sqlite3 as lite
from calendar import monthrange
from datetime import datetime, date, timedelta

import numpy as np
import pycountry_convert as pc
from dateutil.relativedelta import relativedelta
from forex_python.converter import CurrencyRates
import random

DATABASE_NAME = 'JobDetails.db'


# Converts the currency to USD at the historic rate
def convertCurrency(currency, amount, date):
    c = CurrencyRates()

    dollarAmount = c.get_rate(currency, 'USD', date) * float(amount)
    dollarAmount = '%.2f' % dollarAmount

    split = dollarAmount.split('.')
    if (int(split[1]) == 0):
        return split[0]

    return (dollarAmount)


def convertCurrencyWithYear(currency, amount, week, year):
    week = str(year) + "-W" + str(week)

    startDate = datetime.strptime(week + '-1', "%Y-W%W-%w")
    endDate = startDate + relativedelta(weeks=1)

    return getAverage(currency, startDate, endDate, amount)


def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)


def getAverage(currency, startDate, endDate, amount):
    c = CurrencyRates()
    total = 0
    n = 0

    for singleDate in daterange(startDate, endDate):
        total += c.get_rate(currency, 'USD', singleDate)
        n += 1

    average = total / n

    dollarAmount = average * float(amount)
    dollarAmount = '%.2f' % dollarAmount

    split = dollarAmount.split('.')
    if (int(split[1]) == 0):
        return split[0]

    return (dollarAmount)


def calculateWeeklyAverage(currency, amount, weeksAgo):
    today = date.today()
    newDay = (today + relativedelta(weeks=-weeksAgo))

    week = newDay.isocalendar()[1]

    # startDate = datetime.strptime(str(week) + '-1', "%Y-W%W-%w")
    startDate = newDay
    endDate = startDate + relativedelta(weeks=1)

    return getAverage(currency, startDate, endDate, amount)


def calculateMonthlyAverage(currency, amount, monthsAgo):
    today = date.today()
    newDay = (today + relativedelta(months=-monthsAgo))
    month = newDay.month
    year = newDay.year

    startDate = date(year, month, 1)
    endDate = date(year, month, monthrange(year, month)[1])

    return getAverage(currency, startDate, endDate, amount)


def calculateYearlyAverage(currency, amount, year):
    startDate = date(year, 1, 1)
    endDate = date(year + 1, 1, 1)

    return getAverage(currency, startDate, endDate, amount)


# Retrieves saved details to plot
def plotFromDatabase():
    db = "JobDetails.db"
    con = lite.connect(db)
    cur = con.cursor()

    cur.execute('SELECT Country FROM Bids')

    results = cur.fetchall()
    countries = {}

    for item in results:
        country = item[0]
        n = 1
        if (countries.get(country) != None):
            n = countries.get(country) + 1

        countries.update({country: n})

    plotBarChartsOfBidderCountries(countries)


# Generates multiple windows of bar charts to display the countries of bidders - grouped by continent
def plotBarChartsOfBidderCountries(countryValues):
    # Dictionary containing continent codes and continent names
    continents = {
        'NA': 'North America',
        'EU': 'Europe',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Oceania',
        'AF': 'Africa'
    }

    # Dictionary that will hold the data for each country
    countryData = {
        'NA': [[], []],
        'EU': [[], []],
        'SA': [[], []],
        'AS': [[], []],
        'OC': [[], []],
        'AF': [[], []]
    }

    continentPlotData = {
        'North America': 0,
        'Europe': 0,
        'South America': 0,
        'Asia': 0,
        'Oceania': 0,
        'Africa': 0
    }

    # Gets all the countries and the number of bidders from each country
    countries = list(countryValues.keys())
    values = list(countryValues.values())

    # Populating the countryData dictionary with the data from the countries and values lists
    # Grouped by continent
    for i in range(len(countries)):
        country = countries[i]
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")

        continent_code = pc.country_alpha2_to_continent_code(country_code)
        valuesFromContinent = countryData.get(continent_code)

        continentCountries = valuesFromContinent[0]
        continentCountries.append(country)

        continentValues = valuesFromContinent[1]
        continentValues.append(values[i])

        countryData.update({continent_code: [continentCountries, continentValues]})

    continentNames = list(countryData.keys())

    # Plots a graph for each continent
    for name in continentNames:
        data = countryData.get(name)

        if (data != [[], []]):
            countries = data[0]
            values = data[1]

            nameOfContinent = continents.get(name)
            continentPlotData.update({nameOfContinent: sum(values)})

            yPos = np.arange(len(countries))

            fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)

            fig.canvas.set_window_title("Countries of bidders")

            plt.xticks(yPos, sorted(countries), rotation='vertical')

            ax.bar(yPos, values, align='center', alpha=0.5)
            ax.yaxis.set_major_locator(plt.MaxNLocator(20, integer=True))

            plt.ylabel('Number')
            continent_name = continents.get(name)
            plt.title(continent_name)

            # Resizing the graphs to fit in the window
            fig_size = plt.rcParams["figure.figsize"]
            fig_size[0] = 10
            plt.rcParams["figure.figsize"] = fig_size

            plt.tight_layout()

            imageName = "image" + ''.join(char for char in continent_name if char.isalnum()) + ".png"
            plt.savefig(imageName, bbox_inches='tight', dpi=100)

    yPos = np.arange(len(continentPlotData))
    vals = list(continentPlotData.values())

    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
    fig.canvas.set_window_title("Continents")

    ax.bar(yPos, vals, align='center', alpha=0.5)

    plt.xticks(yPos, sorted(list(continentPlotData.keys())), rotation='vertical')
    ax.yaxis.set_major_locator(plt.MaxNLocator(20, integer=True))

    plt.ylabel('Number')
    plt.title("Continents")

    # Resizing the graphs to fit in the window
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10
    plt.rcParams["figure.figsize"] = fig_size

    plt.tight_layout()

    plt.savefig("imageContinents", bbox_inches='tight', dpi=100)

    plt.show()


def doAverages():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('SELECT JobID, AverageBidCost FROM Jobs')

    jobs = cur.fetchall()
    con.commit()

    for job in jobs:
        jobID = job[0]
        cost = job[1]
        if (cost == ''):
            bidAverage = calcAverage(cur, jobID)
            if (bidAverage == -1):
                bidAverage = "None"

            bidAverage = str(str(bidAverage[1]) + str(bidAverage[0]))
            update = "UPDATE Jobs SET AverageBidCost = ? WHERE JobID = ?"
            cur.execute(update, [bidAverage, jobID])
            con.commit()

    cur.execute('SELECT JobID, AverageBidCost FROM ReviewJobs')

    jobs = cur.fetchall()
    con.commit()

    for job in jobs:
        jobID = job[0]
        cost = job[1]
        if (cost == ''):
            bidAverage = calcAverage(cur, jobID)
            if (bidAverage == -1):
                bidAverage = "None"

            bidAverage = str(str(bidAverage[1]) + str(bidAverage[0]))
            update = "UPDATE ReviewJobs SET AverageBidCost = ? WHERE JobID = ?"
            cur.execute(update, [bidAverage, jobID])
            con.commit()


def calcAverage(cur, jobID):
    average = 0.0
    n = 0

    select = "SELECT Price FROM Bids WHERE JobID = ?"
    cur.execute(select, [jobID])

    prices = cur.fetchall()
    for price in prices:
        givenAmount = price[0]
        price = float(''.join(c for c in givenAmount if c.isnumeric() or c == '.'))
        n += 1
        average += price
    try:
        result = average / n
    except ZeroDivisionError:
        return [-1, -1]

    symbol = givenAmount[0]
    return [float('%.2f' % result), symbol]


# Saving values from the database to CSV files
def saveDataToCSV():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    con.commit()

    tables = [each[0] for each in cur.fetchall()]

    bidNames = ["Bid ID", "Job ID", "Country", "User"]
    jobNames = ["Job ID", "URL", "Title", "Description", "Number Of Bidders", "Average Bid Cost", "Final Cost",
                "Currency",
                "Time", "Converted Final Cost", "Country Of Poster", "Country Of Winner", "Year", "Week"]
    profileNames = ["Profile ID", "Username", "Number Of Reviews", "Average Review", "Hourly Rate",
                    "Earnings Percentage",
                    "Country"]
    qualificationNames = ["Qualification ID", "Qualification Type", "User", "Qualification Name", "Extra Information"]
    reviewNames = ["Review ID", "Project URL", "Profile", "Score", "Amount Paid", "Currency", "Converted Currency",
                   "Date Scraped", "Date", "Country", "Notes"]
    winnerNames = ["Job ID", "Job URL", "Username", "Profile URL"]

    names = {"Bids": bidNames, "Jobs": jobNames, "JobsHourly": jobNames, "Profiles": profileNames,
             "Qualifications": qualificationNames, "Reviews": reviewNames, "Winners": winnerNames}

    for table in tables:
        query = "SELECT * FROM " + table
        cur.execute(query)
        data = []

        for item in cur.fetchall():
            data.append(list(item))

        con.commit()

        file = table + ".csv"

        columnNames = names.get(table)

        data.insert(0, columnNames)
        data.insert(1, [])

        for line in data:
            with open(file, 'a', newline='') as fp:
                a = csv.writer(fp, delimiter=',')
                line = [line]
                a.writerows(line)


def scoreProjects(constant, doPrint):
    positive, negative = getKeywords()

    positiveCopy = []

    for word in positive:
        positiveCopy.append(word)
        new = ''.join(c + '.' for c in word if c.isalpha())
        positiveCopy.append(new[:-1])

    positive = positiveCopy


    ratio = (len(positive) * constant) / len(negative)

    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('SELECT JobID, Title, Description FROM Jobs')

    res = cur.fetchall()
    results = []

    for r in res:
        results.append(list(r))

    for i in range(len(results)):
        if doPrint:
            print("Job Score " + str(i + 1) + "/" + str(len(results) + 1))
        job = results[i]
        jID = job[0]
        title = job[1].lower()
        description = job[2].lower()

        posMatches = ""
        negMatches = ""

        numPositive = 0
        numNegative = 0

        for keyword in positive:
            numPositive += (len(title.split(keyword)) - 1) + (len(description.split(keyword)) - 1)
            if (len(title.split(keyword)) > 1) or (len(description.split(keyword)) > 1):
                if (keyword not in posMatches):
                    posMatches += (", " + keyword)

        for keyword in negative:
            numNegative += (len(title.split(keyword)) - 1) + (len(description.split(keyword)) - 1)
            if (len(title.split(keyword)) > 1) or (len(description.split(keyword)) > 1):
                if (keyword not in negMatches):
                    negMatches += (", " + keyword)

        try:
            # numNegative *= ratio
            # l = (numPositive * ratio)
            # score = round((numPositive / (numPositive + numNegative)) * 100)
            score = max(0, round((((numPositive * 100) - (ratio * numNegative)) / (numPositive + numNegative))))
        except ZeroDivisionError:
            score = -1

        p = posMatches.split(",")
        b = ""
        for i in range(len(p)):
            if (i > 0):
                b += p[i]
                if (i != len(p) - 1):
                    b += ", "

        posMatches = b.lstrip()

        n = negMatches.split(",")
        b = ""
        for i in range(len(n)):
            if (i > 0):
                b += n[i]
                if (i != len(n) - 1):
                    b += ", "

        negMatches = b.lstrip()

        query = "UPDATE Jobs SET Score = " + str(score) + \
                ", PositiveMatches = '" + str(posMatches) + "', NegativeMatches = '" + str(
            negMatches) + "' WHERE JobID = " + str(
            jID)
        cur.execute(query)
        con.commit()

    cur.execute('SELECT JobID, Title, Description FROM ReviewJobs')

    res = cur.fetchall()
    results = []

    for r in res:
        results.append(list(r))

    for i in range(len(results)):
        if doPrint:
            print("Review Job Score " + str(i + 1) + "/" + str(len(results) + 1))
        job = results[i]
        jID = job[0]
        title = job[1].lower()
        description = job[2].lower()

        posMatches = ""
        negMatches = ""

        numPositive = 0
        numNegative = 0

        for keyword in positive:
            numPositive += (len(title.split(keyword)) - 1) + (len(description.split(keyword)) - 1)
            if (len(title.split(keyword)) > 1) or (len(description.split(keyword)) > 1):
                if (keyword not in posMatches):
                    posMatches += (", " + keyword)

        for keyword in negative:
            numNegative += (len(title.split(keyword)) - 1) + (len(description.split(keyword)) - 1)
            if (len(title.split(keyword)) > 1) or (len(description.split(keyword)) > 1):
                if (keyword not in negMatches):
                    negMatches += (", " + keyword)

        try:
            # numNegative *= ratio
            # l = (numPositive * ratio)
            # score = round((numPositive / (numPositive + numNegative)) * 100)
            score = max(0, round((((numPositive * 100) - (ratio * numNegative)) / (numPositive + numNegative))))
        except ZeroDivisionError:
            score = -1

        p = posMatches.split(",")
        b = ""
        for i in range(len(p)):
            if (i > 0):
                b += p[i]
                if (i != len(p) - 1):
                    b += ", "

        posMatches = b.lstrip()

        n = negMatches.split(",")
        b = ""
        for i in range(len(n)):
            if (i > 0):
                b += n[i]
                if (i != len(n) - 1):
                    b += ", "

        negMatches = b.lstrip()


        query = "UPDATE ReviewJobs SET Score = " + str(score) + \
                ", PositiveMatches = '" + str(posMatches) + "', NegativeMatches = '" + str(
            negMatches) + "' WHERE JobID = " + str(
            jID)
        cur.execute(query)
        con.commit()


def getKeywords():
    positive = []
    negative = []

    for line in open('positiveKeywords.txt'):
        if (len(line) > 1):
            word = line.rstrip('\n')
            positive.append(word)

    for line in open('negativeKeywords.txt'):
        if (len(line) > 1):
            word = line.rstrip('\n')
            negative.append(word)

    return [keyword.lower() for keyword in positive], [keyword.lower() for keyword in negative]


def conversions():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('''SELECT ReviewID, AmountPaid, Currency, Date FROM Reviews''')

    res = cur.fetchall()

    results = []
    for result in res:
        results.append(list(result))

    for i in range(len(results)):
        print("Review " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        id = r[0]
        value = r[1]
        if (value != 'SEALED'):
            amount = float(''.join(c for c in value if c.isnumeric() or c == '.'))
        else:
            amount = "None"
        currency = r[2]
        dateOff = r[3]
        timeSplit = dateOff.split()
        timeFrame = timeSplit[1]
        timeAmount = int(timeSplit[0])
        convertedCurrency = "None"
        if amount != "None":
            if ((timeFrame == 'month') or (timeFrame == 'months')):
                convertedCurrency = calculateMonthlyAverage(currency, amount, timeAmount)
            elif ((timeFrame == 'week') or (timeFrame == 'weeks')):
                convertedCurrency = calculateWeeklyAverage(currency, amount, timeAmount)
            elif ((timeFrame == 'year') or (timeFrame == 'years')):
                convertedCurrency = calculateYearlyAverage(currency, amount,
                                                           date.today().year - timeAmount)
            elif ((timeFrame == 'day') or (timeFrame == 'days')):
                dateToConvert = date.today() - relativedelta(days=timeAmount)
                convertedCurrency = convertCurrency(currency, amount, dateToConvert)

            convertedCurrency = "$" + str(convertedCurrency)
        query = "UPDATE Reviews SET ConvertedCurrency = '" + str(convertedCurrency) + "' WHERE ReviewID = " + str(id)
        cur.execute(query)
        con.commit()


def jobConversions():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('''SELECT JobID, FinalCost, Currency, Year, Week FROM Jobs''')

    res = cur.fetchall()

    results = []
    for result in res:
        results.append(list(result))

    for i in range(len(results)):
        print("Job " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        id = r[0]
        value = r[1]
        if (value != 'None'):
            amount = float(''.join(c for c in value if c.isnumeric() or c == '.'))
        else:
            amount = "None"
        currency = r[2]
        year = r[3]
        week = r[4]
        convertedCurrency = "None"
        if amount != "None":
            convertedCurrency = convertCurrencyWithYear(currency, amount, week, year)
            convertedCurrency = "$" + str(convertedCurrency)

        query = "UPDATE Jobs SET ConvertedFinalCost = '" + str(convertedCurrency) + "' WHERE JobID = " + str(
            id)
        cur.execute(query)
        con.commit()

    reviewJobConversions()


def reviewJobConversions():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()
    cur.execute('''SELECT JobID, FinalCost, Currency, Date FROM ReviewJobs''')

    res = cur.fetchall()

    results = []
    for result in res:
        results.append(list(result))

    for i in range(len(results)):
        print("Review Job " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        timeSplit = r[3].split()
        timeFrame = timeSplit[1]
        timeAmount = int(timeSplit[0])
        currency = r[2]
        finalCost = r[1]
        convertedCurrency = ""
        jID = r[0]

        if (finalCost != "None"):
            valuePaid = float(''.join(c for c in finalCost if c.isnumeric() or c == '.'))

            if ((timeFrame == 'month') or (timeFrame == 'months')):
                convertedCurrency = calculateMonthlyAverage(currency, valuePaid, timeAmount)
            elif ((timeFrame == 'week') or (timeFrame == 'weeks')):
                convertedCurrency = calculateWeeklyAverage(currency, valuePaid, timeAmount)
            elif ((timeFrame == 'year') or (timeFrame == 'years')):
                convertedCurrency = calculateYearlyAverage(currency, valuePaid,
                                                           date.today().year - timeAmount)
            elif ((timeFrame == 'day') or (timeFrame == 'days')):
                dateToConvert = date.today() - relativedelta(days=timeAmount)
                convertedCurrency = convertCurrency(currency, valuePaid, dateToConvert)

            convertedCurrency = "$" + str(convertedCurrency)

            query = "UPDATE ReviewJobs SET ConvertedFinalCost = '" + str(convertedCurrency) + "' WHERE JobID = " + str(
                jID)
            cur.execute(query)
            con.commit()


def getDateRanges():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    today = date.today()

    cur.execute('SELECT JobID, Date FROM ReviewJobs')

    res = cur.fetchall()

    results = []

    for r in res:
        results.append(list(r))

    for i in range(len(results)):
        print("Review Job Date " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        timeSplit = r[1].split()
        timeFrame = timeSplit[1]
        timeAmount = int(timeSplit[0])
        jID = r[0]

        timeRange = ""

        if ((timeFrame == 'month') or (timeFrame == 'months')):
            newDay = (today + relativedelta(months=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'week') or (timeFrame == 'weeks')):
            newDay = (today + relativedelta(weeks=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'year') or (timeFrame == 'years')):
            newDay = (today + relativedelta(years=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'day') or (timeFrame == 'days')):
            newDay = (today + relativedelta(days=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate

        query = "UPDATE ReviewJobs SET DateRange = '" + str(timeRange) + "' WHERE JobID = " + str(
            jID)
        cur.execute(query)
        con.commit()

    cur.execute('SELECT ReviewID, Date FROM Reviews')

    res = cur.fetchall()

    results = []

    for r in res:
        results.append(list(r))

    for i in range(len(results)):
        print("Review Date " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        timeSplit = r[1].split()
        timeFrame = timeSplit[1]
        timeAmount = int(timeSplit[0])
        jID = r[0]

        timeRange = ""

        if ((timeFrame == 'month') or (timeFrame == 'months')):
            newDay = (today + relativedelta(months=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'week') or (timeFrame == 'weeks')):
            newDay = (today + relativedelta(weeks=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'year') or (timeFrame == 'years')):
            newDay = (today + relativedelta(years=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate
        elif ((timeFrame == 'day') or (timeFrame == 'days')):
            newDay = (today + relativedelta(days=-timeAmount))
            month = newDay.month
            year = newDay.year
            startDate = date(year, month, 1).strftime("%d/%m/%y")
            endDate = date(year, month, monthrange(year, month)[1]).strftime("%d/%m/%y")
            timeRange = startDate + " - " + endDate

        query = "UPDATE Reviews SET DateRange = '" + str(timeRange) + "' WHERE ReviewID = " + str(
            jID)
        cur.execute(query)
        con.commit()

    cur.execute('SELECT JobID, Year, Week FROM Jobs')

    res = cur.fetchall()

    results = []

    for r in res:
        results.append(list(r))

    for i in range(len(results)):
        print("Job Date " + str(i + 1) + "/" + str(len(results) + 1))
        r = results[i]
        year = r[1]
        jobWeek = r[2]
        jID = r[0]
        week = str(year) + "-W" + str(jobWeek)
        startDate = datetime.strptime(week + '-1', "%Y-W%W-%w")
        endDate = startDate + relativedelta(weeks=1)

        timeRange = startDate.strftime("%d/%m/%y") + " - " + endDate.strftime("%d/%m/%y")

        query = "UPDATE Jobs SET DateRange = '" + str(timeRange) + "' WHERE JobID = " + str(
            jID)
        cur.execute(query)
        con.commit()


def optimiseConstant():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    low = 1
    high = 500
    averageDistance = 1000
    constant = random.randrange(low, high + 1)

    iteration = 1

    ranges = {1: [0, 25], 2: [10, 45], 3: [45, 55], 4: [55, 90], 5: [70, 100]}

    while((averageDistance >= 5) and (iteration < 10000)):
        print("Iteration number: " + str(iteration) + " - Constant = " + str(constant))
        tooBig = 0
        tooSmall = 0
        scoreProjects(constant, False)
        averageDistances = []
        for i in range(1, 6):
            totalDistance = 0
            n = 0
            query = 'SELECT Score FROM ReviewJobs WHERE Category = ' + str(i)
            cur.execute(query)
            results = [r[0] for r in cur.fetchall()]

            scoreRange = ranges.get(i)
            lower = scoreRange[0]
            upper = scoreRange[1]

            for result in results:
                n += 1
                if (result != -1):
                    if ((result >= lower) and (result <= upper)):
                        distance = 0
                    elif (result > upper):
                        distance = result - upper
                        tooBig += 1
                    else:
                        distance = lower - result
                        tooSmall += 1
                        # distance = min(abs(result - lower), abs(result - upper))

                    totalDistance += distance


            averageDistances.append(totalDistance / n)

        averageDistance = sum(averageDistances) / 5
        if (averageDistance >= 5):
            if (tooBig > tooSmall):
                constant += 0.1
            else:
                constant -= 0.1
        else:
            iteration += 1


    print(constant)



# doAverages()
# jobConversions()
# conversions()
# getDateRanges()
# scoreProjects(10)
optimiseConstant()