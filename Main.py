from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import sys
from PyQt5 import uic, QtWidgets


mainUI = uic.loadUiType("UIs/main.ui")[0]


class Main(QtWidgets.QMainWindow, mainUI):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnFetch.clicked.connect(self.fetch)
        self.btnExit.clicked.connect(self.exit)

    def createDatabase(self):
        dbName = "Cheating.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Details')
        cur.execute('''CREATE TABLE Details (
        'JobID' INTEGER PRIMARY KEY AUTOINCREMENT,
        'NumberOfBidders' INTEGER NOT NULL,
        'AverageBidCost' INTEGER NOT NULL,
        'Country' TEXT NOT NULL
        );''')

        con.commit()

    def databaseSetup(self):
        dbName = "Cheating.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('SELECT JobID FROM Details')

        # Checks if table exists
        if(len(cur.fetchall()) == 0):
            self.createDatabase()

    def exit(self):
        main.close()

    def fetch(self):
        valid = False
        url = self.edtURL.text()

        # Checking if the user has entered anything in the text box
        if (url == ""):
            QtWidgets.QMessageBox.warning(self, "Invalid Entry", "Please enter a URL!", QtWidgets.QMessageBox.Ok,
                                      QtWidgets.QMessageBox.Ok)
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
                data1 = soup.find("h2")

                # Check if anyone has bid on the job yet
                if (data1.text.split("Need to")[0] == data1.text):
                    division = data1.text.split(" ")

                    self.numFreelancers = division[0] + " " + division[1]
                    self.averagePrice = "Bidding an average of " + division[6]
                    self.lblFreelancers.setText(self.numFreelancers)
                    self.lblAvPrice.setText(self.averagePrice)
                else:
                    self.lblFreelancers.setText("Nobody has bid on this yet")
                    self.lblAvPrice.setText("No bids yet")

                data2 = soup.find_all("span")
                for item in data2:
                    if (item.get("itemprop") == "addressLocality"):
                        b = item.text
                        if (b.split(", ")[0] != b):
                            b = item.text.split(", ")[1]
                        else:
                            b = " ".join(b.split())
                            # b.replace(" ", "")
                        self.country = b.split("\n")[0]
                        self.lblCountry.setText(self.country)
                        break
                self.databaseSetup()

            except requests.exceptions.MissingSchema as e:
                QtWidgets.QMessageBox.warning(self, "Invalid entry", "Please enter a valid URL!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                self.edtURL.setText("")
                self.edtURL.setFocus()

    def keyPressEvent(self, event):
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            self.fetch()


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
app.exec()
