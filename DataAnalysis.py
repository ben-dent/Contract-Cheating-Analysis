import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pycountry_convert as pc
import sqlite3 as lite
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from forex_python.converter import CurrencyRates
import csv

# TODO: Implement saving to CSV

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

# Saving values from the database to a CSV file
def saveDataToCSV(table, data):
    file = table + '.csv'

    with open(file, 'a', newline='') as fp:
        a = csv.writer(fp, delimeter=',')
        data = [data]
        a.writerows(data)
