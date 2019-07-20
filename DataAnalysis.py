import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import sqlite3 as lite


def getData():
    db = "Test.db"
    con = lite.connect(db)
    cur = con.cursor()

    cur.execute('SELECT TestID, TestText FROM Test')
    results = cur.fetchall()

    dict = {}

    for pair in results:
        dict[pair[1]] = pair[0]

    plotBarChartOfBidderCountries(dict)

def plotBarChartOfBidderCountries(countryValues):
    countries = countryValues.keys()
    values = countryValues.values()

    yPos = np.arange(len(countries))

    yTickVals = np.arange(max(values) + 1)

    fig = plt.figure(figsize=(30,10))
    fig.canvas.set_window_title("Countries of bidders")

    plt.bar(yPos, values, align='center', alpha=0.5)
    plt.xticks(yPos, countries)
    plt.yticks(yTickVals)

    plt.tight_layout()

    plt.ylabel('Number')
    plt.title('Countries of bidders')

    plt.show()
    plt.savefig("image.png", bbox_inches='tight', dpi=100)