import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import sqlite3 as lite
import pycountry_convert as pc
import time


def getData():
    db = "Test.db"
    con = lite.connect(db)
    cur = con.cursor()

    cur.execute('SELECT TestID, TestText FROM Test')
    results = cur.fetchall()

    dict = {}

    for pair in results:
        dict[pair[1]] = pair[0]

    plotBarChartsOfBidderCountries(dict)

def plotBarChartsOfBidderCountries(countryValues):
    continents = {
        'NA': 'North America',
        'EU': 'Europe',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Oceania',
        'AF': 'Africa'
    }

    countryData = {
        'NA': [[], []],
        'EU': [[], []],
        'SA': [[], []],
        'AS': [[], []],
        'OC': [[], []],
        'AF': [[], []]
    }

    countries = list(countryValues.keys())
    values = list(countryValues.values())

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

    conts = list(countryData.keys())

    for name in conts:
        data = countryData.get(name)

        if (data != [[], []]):
            countries = data[0]
            values = data[1]

            yPos = np.arange(len(countries))

            yTickVals = np.arange(max(values) + 1)

            fig = plt.figure()
            fig.canvas.set_window_title("Countries of bidders")

            plt.bar(yPos, values, align='center', alpha=0.5)
            plt.xticks(yPos, countries)
            plt.yticks(yTickVals)

            plt.ylabel('Number')
            continent_name = continents.get(name)
            plt.title(continent_name)

            fig_size = plt.rcParams["figure.figsize"]
            fig_size[0] = 10
            plt.rcParams["figure.figsize"] = fig_size

            plt.tight_layout()

            imageName = "image" + continent_name + ".png"
            plt.savefig(imageName, bbox_inches='tight', dpi=100)

    plt.show()

            # imageName = "image" + continent_name + ".png"
            # plt.savefig(imageName, bbox_inches='tight', dpi=100)
