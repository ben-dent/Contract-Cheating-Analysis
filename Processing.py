import sqlite3 as lite
import sys

from PyQt5 import uic, QtWidgets

from DataAnalysis import DATABASE_NAME, saveToCSV, plotBarChartsOfBidderCountries

processingUi = uic.loadUiType("UIs/processingUI.ui")[0]
countryUi = uic.loadUiType("UIs/countryUI.ui")[0]


class Processing(QtWidgets.QMainWindow, processingUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnCountryBids.clicked.connect(self.countryBids)
        self.btnCountryPosters.clicked.connect(self.countryPosters)
        self.btnCountryWinners.clicked.connect(self.countryWinners)
        self.btnCategory.clicked.connect(self.category)
        self.btnCategoryRange.clicked.connect(self.categoryRange)
        self.btnKeyword.clicked.connect(self.keyword)

    def countryBids(self):
        l.processing.close()
        l.launchCountryBids()

    def countryPosters(self):
        l.processing.close()
        l.launchCountryPosters()

    def countryWinners(self):
        l.processing.close()
        l.launchCountryWinners()

    def category(self):
        print("Category")

    def categoryRange(self):
        print("Category Range")

    def keyword(self):
        print("Keyword")


class Country(QtWidgets.QMainWindow, countryUi):
    def __init__(self, processType, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.processType = processType
        title = "Filter By Country - " + self.processType
        self.setWindowTitle(title)
        self.lblTitle.setText(title)

        self.data = {}

        if (self.processType == "Posters"):
            l.cur.execute('SELECT DISTINCT(CountryOfPoster) FROM Jobs')
            self.countries = [each[0] for each in l.cur.fetchall()]

            l.cur.execute('SELECT DISTINCT(CountryOfPoster) FROM ReviewJobs WHERE CountryOfPoster NOT IN (SELECT CountryOfPoster FROM Jobs)')
            self.countries += [each[0] for each in l.cur.fetchall()]
        elif (self.processType == "Winners"):
            l.cur.execute(
                "SELECT DISTINCT(CountryOfWinner) FROM Jobs WHERE CountryOfWinner != 'None'")
            self.countries = [each[0] for each in l.cur.fetchall()]

            l.cur.execute(
                "SELECT DISTINCT(CountryOfWinner) FROM ReviewJobs WHERE CountryOfWinner != 'None' AND CountryOfWinner NOT IN (SELECT CountryOfWinner FROM Jobs)")
            self.countries += [each[0] for each in l.cur.fetchall()]
        else:
            query = 'SELECT DISTINCT(Country) FROM Bids ORDER BY Country'
            l.cur.execute(query)
            self.countries = [each[0] for each in l.cur.fetchall()]

        self.cmbCountries.addItems(sorted(self.countries))

        self.getFreqs()

        self.btnGraph.clicked.connect(self.graph)
        self.btnExport.clicked.connect(self.export)
        self.btnBack.clicked.connect(self.back)

    def getFreqs(self):
        for country in self.countries:
            n = 0
            if (self.processType == "Bids"):
                query = "SELECT Count(BidID) FROM Bids WHERE Country = '" + country + "'"
                l.cur.execute(query)
                n = int(l.cur.fetchone()[0])

            elif (self.processType == "Posters"):
                query = "SELECT Count(JobID) FROM Jobs WHERE CountryOfPoster = '" + country + "'"
                l.cur.execute(query)

                n += int(l.cur.fetchone()[0])

                query = "SELECT Count(JobID) FROM ReviewJobs WHERE CountryOfPoster = '" + country + "'"
                l.cur.execute(query)

                n += int(l.cur.fetchone()[0])
            else:
                query = "SELECT Count(JobID) FROM Jobs WHERE CountryOfWinner = '" + country + "'"
                l.cur.execute(query)

                n += int(l.cur.fetchone()[0])

                query = "SELECT Count(JobID) FROM ReviewJobs WHERE CountryOfWinner = '" + country + "'"
                l.cur.execute(query)

                n += int(l.cur.fetchone()[0])


            self.data.update({country: n})

    def graph(self):
        country = self.cmbCountries.currentText()
        plotBarChartsOfBidderCountries({country: self.data.get(country)})

    def export(self):
        if (self.cmbCountries.currentIndex() == 0):
            QtWidgets.QMessageBox.warning(self, "Please select a country!", "Please select a country!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            country = self.cmbCountries.currentText()
            filter = "Country = '" + country + "'"
            file = self.processType + " - " + self.cmbCountries.currentText() + ".csv"
            saveToCSV([self.processType], '*', filter, file)
            QtWidgets.QMessageBox.information(self, "Exported!", "Exported!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def back(self):
        l.country.close()
        l.launchProcessing()


class Launcher:
    def __init__(self):
        self.con = lite.connect(DATABASE_NAME)
        self.cur = self.con.cursor()

    def launchProcessing(self):
        self.processing = Processing()
        self.processing.show()

    def launchCountryBids(self):
        self.country = Country("Bids")
        self.country.show()

    def launchCountryPosters(self):
        self.country = Country("Posters")
        self.country.show()

    def launchCountryWinners(self):
        self.country = Country("Winners")
        self.country.show()

    def launchCategory(self):
        return

    def launchCategoryRange(self):
        return

    def launchKeyword(self):
        return


app = QtWidgets.QApplication(sys.argv)
l = Launcher()
l.launchProcessing()
app.exec()
