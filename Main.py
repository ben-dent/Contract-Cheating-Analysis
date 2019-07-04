'''

Made by Ben Dent as part of an  Undergraduate Research Opportunities Placement (UROP) at Imperial College London

Code is provided as-is under an MIT License

'''

from bs4 import BeautifulSoup
import requests
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sqlite3 as lite
import sys
from PyQt5 import uic, QtWidgets


mainUI = uic.loadUiType("UIs/main.ui")[0]


class Main(QtWidgets.QMainWindow, mainUI):

    ''' This class handles the window in the application as PyQt requires a class for each program window '''

    # In the constructor, the UI is set up and the buttons are linked to the relevant functions
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.btnFetch.clicked.connect(self.loginToFreelancer)
        self.btnFetch.clicked.connect(self.fetch)
        self.btnExit.clicked.connect(self.exit)
        self.btnCloseBrowser.clicked.connect(self.closeBrowser)

    # Creates the table in the database, which will initially be empty
    def createDatabase(self):
        dbName = "JobDetails.db"
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

    # Sets up the database. Calls the createDatabase function if the table doesn't exist yet
    def databaseSetup(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        # Checks if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Details'")
        if(cur.fetchall() == 0):
            self.createDatabase()

    # Closes the window
    def exit(self):
        main.close()

    # Does all the fetching and handling of the data required
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

                # Checking if the given page is an archived page
                self.archiveCheck = soup.find("span", {"class" : "PageProjectViewLogout-awardedTo-heading"})
                self.archived = False

                # The response will be None if the page is archived
                if (self.archiveCheck != None):
                    self.archived = True

                # Finding the average that freelancers are bidding - the first h2 HTML tag
                self.biddersInfo = soup.find_all("h2")
                self.biddersAndPriceFind = self.biddersInfo[0]

                # Makes sure the bidding info is correct as archived pages use a slightly different format
                if (self.archived):
                    self.biddersAndPriceFind = self.biddersInfo[1]

                # Retrieving the country of the customer
                self.customerCountryFind = soup.find_all("span")

                # Retrieving the tags that the customer gave to their task
                self.givenTags = soup.find_all("a", {"class": "PageProjectViewLogout-detail-tags-link--highlight"})

                # Retrieving the countries of the bidders
                self.bidderCountries = soup.find_all("span", {"class": "FreelancerInfo-flag"})

                # Retrieving the final price for the task if we are looking in the archives
                self.finalPrice = soup.find("div", {"class": "FreelancerInfo-price"})

                # Output the retrieved results
                self.output()

            except requests.exceptions.MissingSchema as e:
                # If an entered URL is not valid, it will show an error and clear the inputs
                QtWidgets.QMessageBox.warning(self, "Invalid entry", "Please enter a valid URL!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                self.edtURL.setText("")
                self.edtURL.setFocus()

    def output(self):
        # Check if anyone has bid on the job yet
        if (self.biddersAndPriceFind.text.split("Need to")[0] == self.biddersAndPriceFind.text):
            division = self.biddersAndPriceFind.text.split(" ")

            self.numFreelancers = division[0] + " " + division[1]
            self.averagePrice = "Bidding an average of " + division[6]
            self.lblFreelancers.setText(self.numFreelancers)
            self.lblAvPrice.setText(self.averagePrice)
        else:
            self.lblFreelancers.setText("Nobody has bid on this yet")
            self.lblAvPrice.setText("No bids yet")

        # Finds the country that the customer is from
        for item in self.customerCountryFind:
            if (item.get("itemprop") == "addressLocality"):
                b = item.text
                if (b.split(", ")[0] != b):
                    b = item.text.split(", ")[1]
                else:
                    b = " ".join(b.split())
                self.country = b.split("\n")[0]
                self.lblCountry.setText(self.country)
                break

        # Makes sure that the database exists
        self.databaseSetup()

        # Defines a dictionary to store the number of bidders from each country that has a bidder
        bidderCountries = {}

        # Saving the locations of bidders and the number from that country into the dictionary
        for each in self.bidderCountries:
            # Gets the country of the bidder
            country = each.contents[1].get("title")

            num = 1

            # Checks if the country is already in the dictionary
            result = bidderCountries.get(country)

            # Incrementing value if country already in dictionary
            if (result != None):
                num = result + 1

            # Updating the dictionary with
            bidderCountries.update({country : num})

        # Temporary outputting of the dictionary
        print(bidderCountries)


    def loginToFreelancer(self):
        # The username and password for the throwaway account I created
        username = "AnalysisProject"
        password = "Project!"

        # Launch the Selenium Firefox browser - Use options.headless as False if you want the popup browser
        options = Options()
        options.headless = False
        self.driver = webdriver.Firefox(options=options)

        # Opens the Freelancer login page
        self.driver.get("https://www.freelancer.co.uk/login")

        # Fills in the username
        userField = self.driver.find_element_by_id("username")
        userField.send_keys(username)

        # Fills in the password
        passwordField = self.driver.find_element_by_id("password")
        passwordField.send_keys(password)

        time.sleep(1)

        # Clicks the submit button
        submitButton = self.driver.find_element_by_id("login_btn")
        submitButton.click()

        time.sleep(4)

        # Navigates to the projects page
        # self.driver.get("https://www.freelancer.co.uk/search/projects/")

        # Navigates to the archives page
        # self.driver.get("https://www.freelancer.co.uk/archives/")

        # soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    # Will crawl through the whole archive
    def crawlWholeArchive(self):
        print("Hello")

    # Will crawl through the archived projects within the given time-frame
    def crawlArchives(self, startYear, startWeek):
        # Get the (zero-indexed) week number
        today = date.today().isocalendar()
        currentWeek = today[2] - 1
        years = today[1] - startYear
        print("Hello")

    # Handles closing the browser and the program
    # Precondition - the browser launched by the program is currently open
    def closeBrowser(self):
        self.driver.close()
        self.exit()

    # Handles the user pressing enter, instead of clicking on the 'Fetch' button
    def keyPressEvent(self, event):
        # The enter key number is 16777220
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            # Calls the fetch function
            self.fetch()

# Runs the application and launches the window
app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
app.exec()
