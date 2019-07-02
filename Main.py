from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import sys
from PyQt4 import QtCore, QtGui, uic

mainUI = uic.loadUiType("UIs/main.ui")[0]

class Main(QtGui.QMainWindow, mainUI):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnFetch.clicked.connect(self.fetch)
        self.btnExit.clicked.connect(self.exit)

    def exit(self):
        main.close()

    def fetch(self):
        valid = False
        url = self.edtURL.text()

        # Checking if the user has entered anythig in the text box
        if (url == ""):
            QtGui.QMessageBox.warning(self, "Invalid Entry", "Please enter a URL!", QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
            self.edtURL.setFocus()
        else:
            valid = True

        if valid:
            # url = "https://www.freelancer.co.uk/projects/word/guide-copy-typing/"

            # Checking if the user entered a valid URL
            try:
                r = requests.get(url)

                soup = BeautifulSoup(r.content, "html.parser")

                # Finding the average that freelancers are bidding - the first h2 HTML tag
                a = soup.find("h2")
                division = a.text.split(" ")

                numFreelancers = division[0] + " " + division[1]
                averagePrice = "Bidding an average of " + division[6]
                self.lblFreelancers.setText(numFreelancers)
                self.lblAvPrice.setText(averagePrice)


            except requests.exceptions.MissingSchema as e:
                QtGui.QMessageBox.warning(self, "Invalid entry", "Please enter a valid URL!", QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)
                self.edtURL.setText("")
                self.edtURL.setFocus()

    def keyPressEvent(self, event):
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            self.fetch()


app = QtGui.QApplication(sys.argv)
main = Main()
main.show()
app.exec()