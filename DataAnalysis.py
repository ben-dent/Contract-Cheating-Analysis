import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pycountry_convert as pc


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

            # Resizing the graphs to fit in the window
            fig_size = plt.rcParams["figure.figsize"]
            fig_size[0] = 10
            plt.rcParams["figure.figsize"] = fig_size

            plt.tight_layout()

            imageName = "image" + continent_name + ".png"
            plt.savefig(imageName, bbox_inches='tight', dpi=100)

    plt.show()