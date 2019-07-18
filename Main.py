'''

Made by Ben Dent as part of an  Undergraduate Research Opportunities Placement (UROP) at Imperial College London

Code is provided as-is under an MIT License

'''

# TODO: Implement historic currency conversion

import math
import sqlite3 as lite
import sys
from datetime import datetime
import time

from bs4 import BeautifulSoup

from PyQt5 import uic, QtWidgets
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from Crawler import *

mainUI = uic.loadUiType("UIs/main.ui")[0]


class Main(QtWidgets.QMainWindow, mainUI):
    ''' This class handles the window in the application as PyQt requires a class for each program window '''

    # In the constructor, the UI is set up and the buttons are linked to the
    # relevant functions
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnFetch.clicked.connect(self.setUpProgram)
        self.btnExit.clicked.connect(self.exit)
        self.btnCloseBrowser.clicked.connect(self.closeBrowser)

        self.dateToday = datetime.today().strftime('%d/%m/%y')

        self.profilesSavedAlready = {}
        self.projectsSavedAlready = {}
        self.seenIDs = {}

        self.profilesSeen = {}
        self.projectsSeen = {}

    # Ensures no duplicate entries in tables
    def getSeen(self):
        self.databaseSetup()
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('SELECT URL, JobID FROM Jobs')
        links = cur.fetchall()

        if (len(links) > 0):
            for link in links:
                self.projectsSavedAlready[link[0]] = True
                self.seenIDs[link[1]] = True

        cur.execute('SELECT Username FROM Profiles')
        users = cur.fetchall()

        if (len(users) > 0):
            for user in users:
                self.profilesSavedAlready[LINK_PREFIX + "/u/" + user[0]] = True

    def setUpProgram(self):
        self.databaseSetup()
        self.getSeen()
        projects = getAllTheRelevantLinks("https://www.freelancer.co.uk/archives/essay-writing/2019-21/")

        for project in projects:
            if (self.projectsSavedAlready.get(project) == None):
                self.fetchDataNonLogin(project)

        a = 1

        # self.loginToFreelancer()
        # # url = "https://www.freelancer.co.uk/u/brkbkrcgl"
        # # url = "https://www.freelancer.co.uk/u/LOSPOS77"
        # url = "https://www.freelancer.co.uk/u/Djdesign"
        # # url = "https://www.freelancer.co.uk/u/Maplegroupcom"
        # self.getInformationFromBidderProfile(url)


    # Creates the Qualifications table in the database, which will initially be empty
    def createQualificationsTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Qualifications')
        cur.execute('''CREATE TABLE Qualifications (
        'QualificationID' INTEGER PRIMARY KEY,
        'QualificationType' TEXT NOT NULL,
        'User' TEXT NOT NULL,
        'QualificationName' TEXT NOT NULL,
        'ExtraInformation' TEXT,
        FOREIGN KEY(User) REFERENCES Profiles(Username)
        );''')

        con.commit()

    # Creates the Reviews table in the database, which will initially be empty
    def createReviewsTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Reviews')
        cur.execute('''CREATE TABLE Reviews (
        'ReviewID' INTEGER PRIMARY KEY,
        'Profile' TEXT NOT NULL,
        'Score' INTEGER NOT NULL,
        'AmountPaid' TEXT NOT NULL,
        'DateScraped' TEXT NOT NULL,
        'Date' TEXT NOT NULL,
        'Country' TEXT NOT NULL,
        'Notes' TEXT NOT NULL,
        FOREIGN KEY(Profile) REFERENCES Profiles(Username)
        );''')

        con.commit()

    # Creates the Jobs table in the database, which will initially be empty
    def createJobsTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Jobs')
        cur.execute('''CREATE TABLE Jobs (
        'JobID' INTEGER PRIMARY KEY,
        'URL' TEXT NOT NULL,
        'NumberOfBidders' INTEGER NOT NULL,
        'AverageBidCost' TEXT NOT NULL,
        'FinalCost' TEXT NOT NULL,
        'CountryOfPoster' TEXT NOT NULL,
        'CountryOfWinner' TEXT NOT NULL
        );''')

        con.commit()

    # Creates the Profiles table in the database, which will initially be empty
    def createProfilesTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Profiles')
        cur.execute('''CREATE TABLE Profiles (
        'ProfileID' INTEGER PRIMARY KEY,
        'Username' TEXT NOT NULL,
        'NumReviews' INTEGER NOT NULL,
        'AverageReview' REAL NOT NULL,
        'HourlyRate' TEXT NOT NULL,
        'EarningsPCT' REAL NOT NULL,
        'Country' TEXT NOT NULL
        );''')

        con.commit()

    # Sets up the database. Calls the createDatabase function if the table
    # doesn't exist yet
    def databaseSetup(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        # Checks if tables exist and creates them if they do not
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Jobs'")
        if (len(cur.fetchall()) == 0):
            self.createJobsTable()

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Profiles'")
        if (len(cur.fetchall()) == 0):
            self.createProfilesTable()

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Qualifications'")
        if (len(cur.fetchall()) == 0):
            self.createQualificationsTable()

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Reviews'")
        if (len(cur.fetchall()) == 0):
            self.createReviewsTable()

    # Will save profile details to the database
    def saveProfileDetails(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('''
        INSERT INTO Profiles(Username, NumReviews, AverageReview, HourlyRate, EarningsPCT, Country) 
        VALUES(?,?,?,?,?,?)''',
        (self.username, self.numReviews, self.reviewAv, self.hourly, self.earningsPCT, self.profileCountry))

        con.commit()

    # Will save qualification details to the database
    def saveQualificationDetails(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('''
        INSERT INTO Qualifications(QualificationType, User, QualificationName, ExtraInformation) 
        VALUES(?,?,?,?)''',
        (self.qualificationType, self.username, self.qualName, self.extraInformation))

        con.commit()

    # Will save review details to the database
    def saveReviewDetails(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('''
        INSERT INTO Reviews(Profile, Score, AmountPaid, DateScraped, Date, Country, Notes) 
        VALUES(?,?,?,?,?,?,?)''',
        (self.username, self.score, self.amountPaid, self.dateToday, self.timePosted, self.reviewCountry, self.note))

        con.commit()

    # Will save job details to the database
    def saveJobDetails(self, url):

        if (not(self.awarded)):
            self.winnerCountry = "None"
            self.finalPrice = "None"

        if (self.numFreelancers == 0):
            self.averagePrice = "None"
            self.finalPrice = "None"

        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('''
        INSERT INTO Jobs(JobID, URL, NumberOfBidders, AverageBidCost, FinalCost, CountryOfPoster, CountryOfWinner) 
        VALUES(?, ?,?,?,?,?,?)''',
        (self.projectID, url, self.numFreelancers, self.averagePrice, self.finalPrice, self.customerCountry, self.winnerCountry))

        con.commit()

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
        self.customerProfileLink = self.driver.find_elements(
            By.CLASS_NAME, "NativeElement.ng-star-inserted")[10].text
        self.customerProfileLink = LINK_PREFIX + "/u/" + \
            self.customerProfileLink.split("@")[1]

    # Fetching all the data that requires a login first
    def fetchDataWithLogin(self):
        profileLinks = list(self.profilesSeen.keys())[:2]
        for profile in profileLinks:
            self.getInformationFromBidderProfile(profile)

    # Fetching all the data that we need without logging in
    def fetchDataNonLogin(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content, "html.parser")

        self.projectID = self.soup.find_all(
            "p", {"class": "PageProjectViewLogout-detail-tags"}
        )[2].text.split("#")[-1]

        if (self.seenIDs.get(self.projectID) == None):

            self.seenIDs[self.projectID] = True
            print("\n" + url)

            # Checking if the given page is an archived page
            self.finishedType = self.soup.find(
                "span", {"class": "promotion-tag"}).text

            # Removing irrelevant characters
            self.finishedType = ''.join(
                c for c in self.finishedType if c.isalnum())

            self.archived = False

            print(self.finishedType)

            # If the project is archived then the response will definitely be
            # one of these
            if (self.finishedType == "Cancelled" or self.finishedType ==
                    "Closed" or self.finishedType == "Completed"):
                self.archived = True

            # Finding the average that freelancers are bidding - the first h2
            # HTML tag
            self.biddersInfo = self.soup.find_all("h2")
            self.biddersAndPriceFind = self.biddersInfo[0]

            if (self.finishedType == "InProgress"):
                if (self.soup.find("span", {"class": "PageProjectViewLogout-awardedTo-heading"}) != None):
                    self.biddersAndPriceFind = self.biddersInfo[1]

            self.awarded = False

            # Checks if the project was awarded to anyone
            if (self.archived and self.finishedType == "Completed"):
                self.awarded = True

                # Makes sure the bidding info is correct as archived pages use
                # a slightly different format
                self.biddersAndPriceFind = self.biddersInfo[1]

                # self.winner = LINK_PREFIX + self.soup.find(
                #     "a", {"class": "FreelancerInfo-username"}).get("href")
                self.winnerCountry = self.soup.find(
                    "span", {"class": "usercard-flag"}).get("title")

                # Retrieving the final price for the task if we are looking at
                # a completed project in the archives
                self.finalPrice = self.soup.find(
                    "div", {"class": "FreelancerInfo-price"}).text

            # Retrieving the tags that the customer gave to their task
            self.givenTags = self.soup.find_all(
                "a", {"class": "PageProjectViewLogout-detail-tags-link--highlight"})

            # Get the country of the customer
            self.getCustomerCountry()

            # Gets the information about the bidders
            self.getBiddersInfo()

            self.saveJobDetails(url)
            a = 1

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

        print("\nCustomer country: " + self.customerCountry + "\n")

    # Gets all information about the bidders then calls getBiddersCountries to
    # get their locations
    def getBiddersInfo(self):
        # A list for the links to the bidders' profiles
        self.bidderProfileLinks = []

        # Adding each link to the bidder profiles to the list
        bidderLinks = self.soup.find_all(
            "a", {"class": "FreelancerInfo-username"})

        for each in bidderLinks:
            self.bidderProfileLinks.append(LINK_PREFIX + each.get("href"))

        # Check if anyone has bid on the job yet
        if (self.biddersAndPriceFind.text.split("Need to")
                [0] == self.biddersAndPriceFind.text):
            division = self.biddersAndPriceFind.text.split(" ")

            self.numFreelancers = division[0]
            self.averagePrice = division[6]
            print(
                self.numFreelancers +
                " freelancers who are bidding an average of " +
                self.averagePrice)

            if (self.awarded):
                print("The final price was: " + self.finalPrice + "\n")
            else:
                print("No one was awarded this project\n")

            self.getBiddersCountries()

            for profile in self.bidderProfileLinks:
                if (self.profilesSeen.get(profile) == None):
                    self.profilesSeen[profile] = True

        else:
            print("No bids yet")

    # Retrieving the countries of the bidders and storing them in a dictionary
    def getBiddersCountries(self):
        # Retrieves all listed countries of the bidders
        self.bidderCountries = self.soup.find_all(
            "span", {"class": "FreelancerInfo-flag"})

        # Defines a dictionary to store the number of bidders from each country
        # that has a bidder
        self.countriesOfBidders = {}

        # Saving the locations of bidders and the number from that country into
        # the dictionary
        for each in self.bidderCountries:
            # Gets the country of the bidder
            country = each.contents[1].get("title")

            num = 1

            # Checks if the country is already in the dictionary
            result = self.countriesOfBidders.get(country)

            # Incrementing value if country already in dictionary
            if (result is not None):
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
        # Go to the bidder profile
        self.driver.get(url)
        time.sleep(3)

        self.profilesSeen[url] = True

        self.username = url.split("/")[-1].split("?")[0]

        # Get their list of certifications
        self.getCertifications()

        z = 1

        self.hourly = self.driver.find_element_by_class_name("PageProfile-info-rate-value").text
        self.profileCountry = self.driver.find_element_by_class_name("profile-location-flag").get_attribute("title")

        # Gets the profile description given by the bidder
        self.profileDescription = self.driver.find_elements(
            By.CLASS_NAME, "profile-about-description")[1].text

        # Getting their average review
        self.reviewAv = self.driver.find_element_by_class_name(
            "Rating").get_attribute("data-star_rating")

        # Get their % of earnings in that category
        self.earningsPCT = float(
            self.driver.find_element_by_class_name("Earnings-label").text) * 10

        # Get the qualifications they give
        qualificationTypes = self.driver.find_elements_by_class_name(
            "profile-experience")
        if (len(qualificationTypes) > 0):
            for item in qualificationTypes:
                sectionName = item.find_element_by_tag_name("h2").text
                self.qualificationType = sectionName
                locationTitle = ""
                if (sectionName == "Experience"):
                    locationTitle = "Working at"
                elif ((sectionName == "Education") or (sectionName == "Qualifications")):
                    locationTitle = "From"
                elif (sectionName == "Publications"):
                    locationTitle = "Published In"

                experienceItems = item.find_elements_by_class_name(
                    "profile-experience-item")

                # print(sectionName + ":")
                for qual in experienceItems:
                    self.qualName = qual.find_element_by_class_name(
                        "profile-experience-title").text
                    self.extraInformation = "None"
                    if (self.qualificationType == "Education"):
                        byline = qual.find_element_by_class_name("profile-experience-byline").text
                        qualDate = qual.find_element_by_class_name("profile-experience-date").text
                        self.extraInformation = byline + ", " + qualDate

                    elif (self.qualificationType == "Qualifications"):
                        self.extraInformation = qual.find_element_by_tag_name("p").text

                    elif (self.qualificationType == "Experience"):
                        byline = qual.find_element_by_class_name("profile-experience-byline").text
                        qualDate = qual.find_element_by_class_name("profile-experience-date").text
                        description = qual.find_element_by_tag_name("p").text
                        self.extraInformation = byline + ", " + qualDate + ", " + description

                    elif (self.qualificationType == "Publications"):
                        byline = qual.find_element_by_class_name("profile-experience-byline").text
                        description = qual.find_element_by_tag_name("p").text
                        self.extraInformation = byline + ", " + description

                    self.saveQualificationDetails()

                    a = 1

                    # print("\n" + qualName)
                    # print(locationTitle + ": " + qual.find_element_by_tag_name("span").text)
                    # try:
                    #     description = qual.find_element_by_tag_name("p").text
                    #     # print("\nDescription: " + description)
                    # except NoSuchElementException:
                    #     hasDescription = False

                # print("\n#########\n")

        # Get all the details on the reviews
        self.getReviewDetails()

        time.sleep(3)

        # Get the job stats from the right hand side bar
        statList = self.driver.find_element_by_class_name("item-stats")

        stats = statList.find_elements_by_class_name("item-stats-stat")

        self.dict = {}

        # Store all these job stats in a dictionary
        for stat in stats:
            name = stat.find_element_by_class_name(
                "item-stats-name").find_element_by_class_name("ng-scope").text
            pctScore = stat.find_element_by_class_name("item-stats-value").text
            self.dict[name] = pctScore

        # Fetch the review stats
        starsList = self.driver.find_element_by_class_name(
            "user-modal-criteria")

        self.starsDict = {}

        firstStar = starsList.find_element_by_class_name("Rating")

        self.starsDict["Quality of Work"] = firstStar.get_attribute(
            "data-star_rating")

        stars = starsList.find_elements_by_class_name("Rating")[1:]
        titlesList = starsList.find_elements_by_class_name(
            "reviews-modal-criteria-key")

        # Store the review stats in a dictionary
        for i in range(len(stars)):
            self.starsDict[titlesList[i].text] = stars[i].get_attribute(
                "data-star_rating")

    # Retrieves all the certifications from the "Certifications" tab
    def getCertifications(self):
        # Goes to the sidebar
        certsList = self.driver.find_element_by_class_name("profile-side-list")

        certs = certsList.find_elements_by_tag_name("li")

        self.certsDict = {}

        # Add to qualification dictionary
        for qual in certs:
            name = qual.find_element_by_class_name("skill-exam-link").text
            score = qual.find_element_by_class_name("skill-exam-value").text
            self.certsDict[name] = score

    # Retrieves details on the reviews on the given bidder profile
    def getReviewDetails(self):
        numDiscounted = 0

        # Expand to get all reviews
        self.driver.find_element(
            By.CLASS_NAME,
            "profile-reviews-btn-top").click()

        time.sleep(3)

        # wait = WebDriverWait(self.driver, 10)

        # Showing the maximum number of reviews possible per page
        dropDownList = self.driver.find_elements(
            By.CLASS_NAME, "small-select")[-1]
        dropDownList.find_elements(By.TAG_NAME, "option")[-1].click()

        time.sleep(3)

        # Get the number of reviews given to this worker
        self.numReviewsToOutput = self.driver.find_element_by_tag_name(
            "ng-pluralize").text
        self.numReviews = int(self.numReviewsToOutput.split(" ")[0])

        self.saveProfileDetails()

        done = False
        page = 0

        links = {}
        duplicates = 0

        dupes = []

        # Will loop through all review pages until every review has been seen
        while (not done):
            try:
                emptyCheck = self.driver.find_element_by_class_name(
                    "user-review-empty")
                done = True
            except NoSuchElementException:
                done = False

            # Finds the list of reviews
            reviewList = self.driver.find_element(
                By.CLASS_NAME, "user-reviews")
            reviews = reviewList.find_elements(By.CLASS_NAME, "user-review")

            if (page == math.floor(self.numReviews / 100)):
                reviews = reviews[:(self.numReviews % 100)]

            # Go through all the reviews on the current page
            for i in range(len(reviews)):
                countReview = True
                duplicate = False
                sealed = False
                review = reviews[i]

                # Gathering the score of the review out of 5.0
                scoreElement = review.find_element(
                    By.CLASS_NAME, "user-review-controls")

                self.score = scoreElement.find_element(
                    By.CLASS_NAME, "Rating").get_attribute("data-star_rating")

                # Gathering the amount paid for that project
                amountElement = review.find_element(
                    By.CLASS_NAME, "user-review-price")

                value = amountElement.find_element_by_class_name(
                    "ng-binding").text
                self.amountPaid = value + " " + amountElement.text

                self.reviewCountry = review.find_element_by_class_name("user-review-flag").get_attribute("title")
                self.timePosted = review.find_element_by_class_name("user-review-details").text.split(".")[1].lstrip()

                if (self.amountPaid == " "):
                    countReview = False
                    sealed = True

                # Gets the review text
                reviewText = review.find_element_by_tag_name(
                    "p").text.split('"')[1:][:-1][0]

                # Gets the link to the project that the review is for
                self.projectLink = review.find_element_by_class_name(
                    "user-review-title").get_attribute("href")

                if (links.get(self.projectLink) is None):
                    links[self.projectLink] = True
                else:
                    duplicate = True

                # Temporary output of the extracted data
                print("Review " + str(i + 1 + (page * 100)) +
                      " / " + str(self.numReviewsToOutput))

                saveReview = True

                self.note = "None"

                if (countReview == False):
                    numDiscounted += 1
                    if (sealed):
                        self.note += "Sealed"

                    if (duplicate):
                        saveReview = False

                if (saveReview):
                    self.saveReviewDetails()

                a = 1
                # print("Score: " + score)
                # print("\nWith review of:\n" + reviewText)
                # print("\nAmount paid: " + amountPaid)
                # print("\nProject link: " + projectLink)
                # print("\n###########\n")

            # Checks if there are more pages of reviews to look at
            pageCheck = self.driver.find_element_by_class_name(
                "user-reviews-navMeta").text
            pageCheck = pageCheck.split(" ")

            areMorePages = pageCheck[3] != pageCheck[5]

            # If there are more pages of reviews, go and look at them
            if (areMorePages):
                # Makes sure the 'next page' button is clicked if there are
                # more pages of reviews to see
                pageButtons = self.driver.find_element_by_class_name(
                    "user-reviews-pagination")
                page += 1
                nextPageButton = pageButtons.find_elements_by_tag_name(
                    "li")[-2]
                nextPageButton.find_element_by_tag_name("a").click()
                time.sleep(1.5)
            else:
                done = True

                for project in (list(links.keys())):
                    if self.projectsSeen.get(project) == None:
                        self.projectsSeen[project] = True


        # print(str(duplicates) + " duplicates")

    # Handles logging into the site
    def loginToFreelancer(self):
        # The username and password for the throwaway account I created - Feel
        # free to make your own
        username = "AnalysisProject"
        password = "Project!"

        # Launch the Selenium Firefox browser
        # Use options.headless as False if you want the popup browser, True
        # otherwise
        options = Options()
        options.headless = True

        # Creating the browser instance
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(20)

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

    # Handles the user pressing enter, instead of clicking on the 'Fetch'button
    def keyPressEvent(self, event):
        # The enter key number is 16777220
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            # Calls the fetch function
            self.setUpProgram()


# Runs the application and launches the window
app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
app.exec()
