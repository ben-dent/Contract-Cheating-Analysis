import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np


def plotBarChartOfBidderCountries(countryValues):
    countries = countryValues.keys()
    values = countryValues.values()

    y_pos = np.arange(len(countries))

    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, countries)
    plt.ylabel('Number')
    plt.title('Countries of bidders')

    plt.show()


dict = {'United Kingdom': 2, 'United States': 4, 'Canada': 5, 'Australia': 10}
plotBarChartOfBidderCountries(dict)