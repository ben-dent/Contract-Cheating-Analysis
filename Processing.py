import sys
from PyQt5 import uic, QtWidgets

processingUi = uic.loadUiType("UIs/processingUI.ui")[0]

class Processing(QtWidgets.QMainWindow, processingUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnCountry.clicked.connect(self.country)
        self.btnCategory.clicked.connect(self.category)
        self.btnCategoryRange.clicked.connect(self.categoryRange)
        self.btnKeyword.clicked.connect(self.keyword)

    def country(self):
        l.processing.close()
        l.launchCountry()

    def category(self):
        print("Category")

    def categoryRange(self):
        print("Category Range")

    def keyword(self):
        print("Keyword")


countryUi = uic.loadUiType("UIs/countryUI.ui")[0]

class Country(QtWidgets.QMainWindow, countryUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnGraph.clicked.connect(self.graph)
        self.btnExport.clicked.connect(self.export)
        self.btnBack.clicked.connect(self.back)

    def graph(self):
        print("Graph")

    def export(self):
        print("Export")

    def back(self):
        l.country.close()
        l.launchProcessing()

class Launcher:

    def launchProcessing(self):
        self.processing = Processing()
        self.processing.show()

    def launchCountry(self):
        self.country = Country()
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