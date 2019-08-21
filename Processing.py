import sqlite3 as lite
import sys

from PyQt5 import uic, QtWidgets

from DataAnalysis import DATABASE_NAME, saveToCSV

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
        print("Country - Posters")

    def countryWinners(self):
        print("Country - Winners")

    def category(self):
        print("Category")

    def categoryRange(self):
        print("Category Range")

    def keyword(self):
        print("Keyword")


class CountryBids(QtWidgets.QMainWindow, countryUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        l.cur.execute('SELECT DISTINCT(Country) FROM Bids ORDER BY Country')
        countries = [each[0] for each in l.cur.fetchall()]
        self.cmbCountries.addItems(countries)

        self.btnGraph.clicked.connect(self.graph)
        self.btnExport.clicked.connect(self.export)
        self.btnBack.clicked.connect(self.back)

    def graph(self):
        print("Graph")

    def export(self):
        if (self.cmbCountries.currentIndex() == 0):
            QtWidgets.QMessageBox.warning(self, "Please select a country!", "Please select a country!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            filter = "Country = '" + self.cmbCountries.currentText() + "'"
            saveToCSV("Bids", '*', filter)

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
        self.country = CountryBids()
        self.country.show()

    def launchCountryPosters(self):
        return

    def launchCountryWinners(self):
        return

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
