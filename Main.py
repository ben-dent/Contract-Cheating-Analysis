'''

Made by Ben Dent as part of an  Undergraduate Research Opportunities Placement (UROP) at Imperial College London

Code is provided as-is under an MIT License

'''

# TODO: Add customer profile link to links to view - but in a different way
# TODO: Scrape details from profiles
# TODO: Scrape review details from right sidebar

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sqlite3 as lite
import sys
from PyQt5 import uic, QtWidgets

from Crawler import *
from DataAnalysis import *


mainUI = uic.loadUiType("UIs/main.ui")[0]


class Main(QtWidgets.QMainWindow, mainUI):

    ''' This class handles the window in the application as PyQt requires a class for each program window '''

    # In the constructor, the UI is set up and the buttons are linked to the relevant functions
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnFetch.clicked.connect(self.check)
        self.btnExit.clicked.connect(self.exit)
        self.btnCloseBrowser.clicked.connect(self.closeBrowser)

    def check(self):
        self.loginToFreelancer()
        # url = "https://www.freelancer.co.uk/u/brkbkrcgl"
        # url = "https://www.freelancer.co.uk/u/LOSPOS77"
        url = "https://www.freelancer.co.uk/u/Djdesign"
        self.getInformationFromBidderProfile(url)
        self.projectsToLookAt = []

    def test(self):
        linksToLookAt = getThisYearApartFromLastMonth("https://www.freelancer.co.uk/archives/essay-writing/")
        for project in linksToLookAt:
            self.fetchDataNonLogin(project)
            b = 1
        self.loginToFreelancer()
        a = 1
        # crawlArchiveByGivenURL("https://www.freelancer.co.uk/archives/dot-net/", 1)

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
        'FinalCost' INTEGER NOT NULL,
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
        url = "https://www.freelancer.co.uk/projects/graphic-design/Photos-for-Radio-Promo/"

        # Fetch the data that can be gathered without logging in
        self.fetchDataNonLogin(url)

        # Login
        self.loginToFreelancer()

        # Fetch the data that requires logging in
        self.fetchDataWithLogin(url)

    # Retrieves the profile link of the customer who posted the job
    def getCustomerProfileLink(self):
        self.customerProfileLink = self.driver.find_elements(By.CLASS_NAME, "NativeElement.ng-star-inserted")[10].text
        self.customerProfileLink = LINK_PREFIX + "/u/" + self.customerProfileLink.split("@")[1]

    # Fetching all the data that requires a login first
    def fetchDataWithLogin(self, url):
        # Open the project page
        self.driver.get(url)
        time.sleep(4)

        # Get the profile link for the customer who posted the task (if it shows it to you)
        if (self.driver.current_url.split("/")[-1] == "reviews"):
            self.getCustomerProfileLink()
            print("Gathered customer profile link")
        else:
            print("Could not gather customer profile link")

    # Fetching all the data that we need without logging in
    def fetchDataNonLogin(self, url):
        # Checking if the user entered a valid URL
        try:
            r = requests.get(url)
            self.soup = BeautifulSoup(r.content, "html.parser")

            # Checking if the given page is an archived page
            self.finishedType = self.soup.find("span", {"class": "promotion-tag"}).text

            # Removing irrelevant characters
            self.finishedType = ''.join(c for c in self.finishedType if c.isalnum())

            self.archived = False

            # If the project is archived then the response will definitely be one of these
            if (self.finishedType == "Cancelled" or self.finishedType == "Closed" or self.finishedType == "Completed"):
                self.archived = True

            # Finding the average that freelancers are bidding - the first h2 HTML tag
            self.biddersInfo = self.soup.find_all("h2")
            self.biddersAndPriceFind = self.biddersInfo[0]

            self.awarded = False

            # Checks if the project was awarded to anyone
            if (self.archived and self.finishedType == "Completed"):
                self.awarded = True

                # Makes sure the bidding info is correct as archived pages use a slightly different format
                self.biddersAndPriceFind = self.biddersInfo[1]

                # Retrieving the final price for the task if we are looking at a completed project in the archives
                self.finalPrice = self.soup.find("div", {"class": "FreelancerInfo-price"}).text

            # Retrieving the tags that the customer gave to their task
            self.givenTags = self.soup.find_all("a", {"class": "PageProjectViewLogout-detail-tags-link--highlight"})

            # Get the country of the customer
            self.getCustomerCountry()

            # Gets the information about the bidders
            self.getBiddersInfo()

        except requests.exceptions.MissingSchema as e:
            # If an entered URL is not valid, it will show an error and clear the inputs
            QtWidgets.QMessageBox.warning(self, "Invalid entry", "Please enter a valid URL!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.edtURL.setText("")
            self.edtURL.setFocus()

    # Retrieving the country of the customer
    def getCustomerCountry(self):
        self.customerCountryFind = self.soup.find_all("span")

        # Finds the country that the customer is from
        for item in self.customerCountryFind:
            if (item.get("itemprop") == "addressLocality"):
                countryParts = item.text
                if (countryParts.split(", ")[0] != countryParts):
                    countryParts = item.text.split(", ")[1]
                else:
                    countryParts = " ".join(countryParts.split())
                self.customerCountry = countryParts.split("\n")[0]
                break

        print("Customer country: " + self.customerCountry + "\n")

    # Gets all information about the bidders then calls getBiddersCountries to get their locations
    def getBiddersInfo(self):
        # A list for the links to the bidders' profiles
        self.bidderProfileLinks = []

        # Adding each link to the bidder profiles to the list
        bidderLinks = self.soup.find_all("a", {"class": "FreelancerInfo-username"})
        for each in bidderLinks:
            self.bidderProfileLinks.append(LINK_PREFIX + each.get("href"))

        # Check if anyone has bid on the job yet
        if (self.biddersAndPriceFind.text.split("Need to")[0] == self.biddersAndPriceFind.text):
            division = self.biddersAndPriceFind.text.split(" ")

            self.numFreelancers = division[0]
            self.averagePrice = division[6]
            print(self.numFreelancers + " freelancers who are bidding an average of " + self.averagePrice)

            if (self.awarded):
                print("The final price was: " + self.finalPrice + "\n")
            else:
                print("No one was awarded this project\n")

            self.getBiddersCountries()

        else:
            print("No bids yet")

    # Retrieving the countries of the bidders and storing them in a dictionary
    def getBiddersCountries(self):
        # Retrieves all listed countries of the bidders
        self.bidderCountries = self.soup.find_all("span", {"class": "FreelancerInfo-flag"})

        # Defines a dictionary to store the number of bidders from each country that has a bidder
        self.countriesOfBidders = {}

        # Saving the locations of bidders and the number from that country into the dictionary
        for each in self.bidderCountries:
            # Gets the country of the bidder
            country = each.contents[1].get("title")

            num = 1

            # Checks if the country is already in the dictionary
            result = self.countriesOfBidders.get(country)

            # Incrementing value if country already in dictionary
            if (result != None):
                num = result + 1

            # Updating the dictionary with
            self.countriesOfBidders.update({country: num})

        # Temporary outputting of the dictionary
        print("Countries of bidders: ")

        for key in self.countriesOfBidders.keys():
            print(key + ": " + str(self.countriesOfBidders.get(key)))

        self.databaseSetup()

    # Extracts the information from the profile of the bidder
    def getInformationFromBidderProfile(self, url):

        # TODO: Get data from all the various sections of certification

        self.driver.get(url)
        time.sleep(3)

        # Gets the profile description given by the bidder
        profileDescription = self.driver.find_elements(By.CLASS_NAME, "profile-about-description")[1].text

        reviewAv = self.driver.find_element_by_class_name("Rating").get_attribute("data-star_rating")

        earningsPCT = float(self.driver.find_element_by_class_name("Earnings-label").text) * 10

        # Get all the details on the reviews
        # self.getReviewDetails()

        qualificationTypes = self.driver.find_elements_by_class_name("profile-experience")
        if (len(qualificationTypes) > 0):
            for item in qualificationTypes:
                sectionName = item.find_element_by_tag_name("h2").text
                locationTitle = ""
                if (sectionName == "Experience"):
                    locationTitle = "Working at"
                elif ((sectionName == "Education") or (sectionName == "Qualifications")):
                    locationTitle = "From"
                elif (sectionName == "Publications"):
                    locationTitle = "Published In"

                experienceItems = item.find_elements_by_class_name("profile-experience-item")

                # print(sectionName + ":")
                for qual in experienceItems:
                    qualName = qual.find_element_by_class_name("profile-experience-title").text
                    # print("\n" + qualName)
                    # print(locationTitle + ": " + qual.find_element_by_tag_name("span").text)
                    try:
                        description = qual.find_element_by_tag_name("p").text
                        # print("\nDescription: " + description)
                    except NoSuchElementException:
                        hasDescription = False

                # print("\n#########\n")


        # TODO: Get retrieval of stats working

        self.driver.find_element(By.CLASS_NAME, "profile-reviews-btn-top").click()

        time.sleep(3)

        statList = self.driver.find_element_by_class_name("item-stats")

        stats = statList.find_elements_by_class_name("item-stats-stat")

        dict = {}

        for stat in stats:
            name = stat.find_element_by_class_name("item-stats-name").find_element_by_class_name("ng-scope").text
            pctScore = stat.find_element_by_class_name("item-stats-value").text
            dict[name] = pctScore

        numReviewsToOutput = self.driver.find_elements_by_class_name("Rating-review")[2].text

        starsList = self.driver.find_element_by_class_name("user-modal-criteria")

    # Retrieves details on the reviews on the given bidder profile
    def getReviewDetails(self):
        # Expand to get all reviews
        self.driver.find_element(By.CLASS_NAME, "profile-reviews-btn-top").click()

        time.sleep(3)

        # Showing the maximum number of reviews possible per page
        dropDownList = self.driver.find_elements(By.CLASS_NAME, "small-select")[-1]
        dropDownList.find_elements(By.TAG_NAME, "option")[-1].click()

        time.sleep(3)

        # Checks if there are more pages of reviews to look at
        pageCheck = self.driver.find_element_by_class_name("user-reviews-navMeta").text
        pageCheck = pageCheck.split(" ")
        areMorePages = pageCheck[3] != pageCheck[5]

        done = False

        # Will loop through all review pages until every review has been seen
        while (not done):
            # Finds the list of reviews
            reviewList = self.driver.find_element(By.CLASS_NAME, "user-reviews")
            reviews = reviewList.find_elements(By.CLASS_NAME, "user-review")

            # Go through all the reviews on the current page
            for review in reviews:
                # Gathering the score of the review out of 5.0
                scoreElement = review.find_element(By.CLASS_NAME, "user-review-controls")
                score = scoreElement.find_element(By.CLASS_NAME, "Rating").get_attribute("data-star_rating")

                # Gathering the amount paid for that project
                amountElement = review.find_element(By.CLASS_NAME, "user-review-price")
                value = amountElement.find_element_by_class_name("ng-binding").text
                amountPaid = value + " " + amountElement.text

                # Gets the review text
                reviewText = review.find_element_by_tag_name("p").text.split('"')[1:][:-1][0]

                # Gets the link to the project that the review is for
                projectLink = review.find_element_by_class_name("user-review-title").get_attribute("href")

                # Temporary output of the extracted data
                print("Score: " + score)
                print("\nWith review of:\n" + reviewText)
                print("\nAmount paid: " + amountPaid)
                print("\nProject link: " + projectLink)
                print("\n###########\n")

            # If there are more pages of reviews, go and look at them
            if (areMorePages):
                # Makes sure the 'next page' button is clicked if there are more pages of reviews to see
                pageButtons = self.driver.find_element_by_class_name("user-reviews-pagination")
                nextPageButton = pageButtons.find_elements_by_tag_name("li")[-2]
                nextPageButton.find_element_by_tag_name("a").click()
                time.sleep(3)
            else:
                done = True

    # Handles logging into the site
    def loginToFreelancer(self):
        # The username and password for the throwaway account I created - Feel free to make your own
        username = "AnalysisProject"
        password = "Project!"

        # Launch the Selenium Firefox browser
        # Use options.headless as False if you want the popup browser, True otherwise
        options = Options()
        options.headless = True

        # Creating the browser instance
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

    # Handles closing the browser and the program
    def closeBrowser(self):
        # Checks if browser is actually open and closes it if it is open
        if (hasattr(self, 'driver')):
            self.driver.close()

        # Close the program
        self.exit()

    # Handles the user pressing enter, instead of clicking on the 'Fetch' button
    def keyPressEvent(self, event):
        # The enter key number is 16777220
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            # Calls the fetch function
            self.check()

# Runs the application and launches the window
app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
app.exec()
