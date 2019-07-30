import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pycountry_convert as pc
import sqlite3 as lite

# TODO: Fix x axis label spacing
# TODO: Implement saving to CSV

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

            plt.xticks(yPos, countries)

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

    plt.xticks(yPos, list(continentPlotData.keys()))
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

def saveDataToDatabase(countryValues):
    file = 'CountryData.csv'

# plotFromDatabase()
