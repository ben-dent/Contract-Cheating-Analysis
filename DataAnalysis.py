import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pycountry_convert as pc
import sqlite3 as lite
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from forex_python.converter import CurrencyRates
import csv
import string

DATABASE_NAME = 'JobDetails.db'

# Converts the currency to USD at the historic rate
def convertCurrency(currency, amount, date):
    c = CurrencyRates()

    dollarAmount = c.get_rate(currency, 'USD', date) * float(amount)
    dollarAmount = '%.2f' % dollarAmount

    split = dollarAmount.split('.')
    if (int(split[1]) == 0):
        return split[0]

    return(dollarAmount)


def convertCurrencyWithYear(currency, amount, week, year):
    week = str(year) + "-W" + str(week)

    startDate = datetime.strptime(week + '-1', "%Y-W%W-%w")
    endDate = startDate + timedelta(days=6)

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
    endDate = startDate + timedelta(days=6)

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

        countryData.update({continent_code : [continentCountries, continentValues]})

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


def extractRelevantProjects():
    tags, keywords = getKeywords()

    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('SELECT * FROM Jobs')
    con.commit()

    jobsToLookAt = []
    data = []
    for result in cur.fetchall():
        data.append(list(result))

    for job in data:
        decided = False
        jobTags = [i.lower() for i in job[4].split(',')]
        tagOverlap = [tag for tag in tags if tag in jobTags]
        if (len(tagOverlap) > 0):
            jobsToLookAt.append(job)
            decided = True

        if (not decided):
            description = job[3]
            words = [i.translate(str.maketrans('', '', string.punctuation)).lower() for i in description]
            keywordOverlap = [k for k in keywords if k in words]
            if (len(keywordOverlap) > 0):
                jobsToLookAt.append(job)
                decided = True

    for values in data:
        cur.execute('''
            INSERT INTO RelevantJobs(JobID, URL, Title, Description, Tags, NumberOfBidders, AverageBidCost, FinalCost,
            Currency, Time, ConvertedFinalCost, CountryOfPoster, CountryOfWinner, Year, Week) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    tuple(values))
        con.commit()


def getKeywords():
    tags = []
    keywords = []
    typeOn = "tags"

    for line in open('potentialKeywords.txt'):
        if (len(line) > 1):
            word = line.rstrip('\n')
            if word == "Keywords:":
                typeOn = "keywords"
            elif word == word.split(':')[0]:
                if (typeOn == "tags"):
                    tags.append(word)
                else:
                    keywords.append(word)
    return [tag.lower() for tag in tags], [keyword.lower() for keyword in keywords]


def conversions():
    con = lite.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute('''SELECT ReviewID, AmountPaid, Currency, Date FROM Reviews''')

    res = cur.fetchall()

    results = []
    for result in res:
        results.append(list(result))

    for r in results:
        id = r[0]
        value = r[1]
        amount = float(''.join(c for c in value if c.isnumeric() or c == '.'))
        currency = r[2]
        date = r[3]
        timeSplit = date.split()
        timeFrame = timeSplit[1]
        timeAmount = int(timeSplit[0])

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
        query = 'UPDATE Reviews SET ConvertedCurrency = ' + str(convertedCurrency) + 'WHERE JobID = ' + str(id)
        cur.execute(query)
        con.commit()


def saveRelevantJobs():
    return


conversions()
