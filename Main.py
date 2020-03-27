"""

Made by Ben Dent as part of an  Undergraduate Research Opportunities Placement (UROP) at Imperial College London

Code is provided as-is under an MIT License

"""

import math
import sys
import time

from PyQt5 import uic, QtWidgets
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from Crawler import *
from DataAnalysis import *
from Notification import sendMessages

mainUI = uic.loadUiType("UIs/main.ui")[0]


# noinspection PyPep8Naming
class Main(QtWidgets.QMainWindow, mainUI):
    """ This class handles the window in the application as PyQt requires a class for each program window """

    # In the constructor, the UI is set up and the buttons are linked to the
    # relevant functions
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnFetch.clicked.connect(self.setUpProgram)
        self.btnExit.clicked.connect(self.exit)
        self.btnCloseBrowser.clicked.connect(self.closeBrowser)
        self.btnSaveCSV.clicked.connect(saveAllDataToCSV)

        self.dateToday = datetime.today().strftime('%d/%m/%y')
        self.time = ''
        self.startFrom = 0
        self.convertedPrice = ""

        self.profilesSavedAlready = {}
        self.projectsSavedAlready = {}
        self.seenIDs = {}

        self.profilesSeen = {}
        self.projectsSeen = {}

        self.finalPrices = []
        self.fetchMode = "First"

        self.winnerProfiles = []
        self.winnerCountries = {}

        self.projectDescription = ""

        # Defines a dictionary to store the number of bidders from each country
        # that has a bidder
        self.countriesOfBidders = {}

        self.numOn = 1
        self.messages = sendMessages()
        self.databaseSetup()

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

        cur.execute('SELECT URL, JobID FROM ReviewJobs')
        links = cur.fetchall()

        if (len(links) > 0):
            for link in links:
                self.projectsSavedAlready[link[0]] = True
                self.seenIDs[link[1]] = True

        cur.execute('SELECT Username FROM Profiles')
        users = cur.fetchall()

        if (len(users) > 0):
            for user in users:
                profileLink = LINK_PREFIX + "/u/" + user[0]
                self.profilesSavedAlready[profileLink] = True
                self.winnerProfiles.append(profileLink)

    def setUpProgram(self):
        self.databaseSetup()
        self.getSeen()
        # projects = getAllTheRelevantLinks("https://www.freelancer.co.uk/archives/essay-writing/2019-21/")
        # url = "https://www.freelancer.co.uk/archives/essay-writing/2019-22/"
        url = "https://www.freelancer.co.uk/archives/essay-writing/2019-17/"
        pageTime = url.split("/")[-2].split("-")
        self.year = int(pageTime[0])
        self.week = int(pageTime[1])
        projects = getAllTheRelevantLinks(url)

        for project in projects:
            if (self.projectsSavedAlready.get(project) is None):
                self.fetchDataNonLogin(project, [])

        self.lookAtWinnerProfiles()

        # plotBarChartsOfBidderCountries(self.winnerCountries)
        # plotBarChartsOfBidderCountries(self.countriesOfBidders)
        doAverages()
        print("\nDone\n")
        self.databaseSetup()
        self.messages.sendMessage()
        # a = 1

        # self.loginToFreelancer()
        # # url = "https://www.freelancer.co.uk/u/brkbkrcgl"
        # # url = "https://www.freelancer.co.uk/u/LOSPOS77"
        # url = "https://www.freelancer.co.uk/u/Djdesign"
        # # url = "https://www.freelancer.co.uk/u/Maplegroupcom"
        # self.getInformationFromBidderProfile(url

    def lookAtMissedReviews(self):
        con = lite.connect(DATABASE_NAME)
        cur = con.cursor()

        results = []

        for table in ['Winners', 'Profiles']:
            query = 'SELECT Username FROM ' + table
            cur.execute(query)
            results += [each[0] for each in cur.fetchall()]

    def getMissed(self):
        self.getSeen()
        con = lite.connect(DATABASE_NAME)
        cur = con.cursor()

        cur.execute(
            'SELECT ProjectURL FROM Reviews WHERE ProjectURL NOT IN ((SELECT URL FROM ReviewJobs) OR (SELECT URL FROM Jobs))')
        results = [each[0] for each in cur.fetchall()]

        for project in results:
            if (self.projectsSavedAlready.get(project) is None):
                self.fetchDataNonLogin(project, [])

    # Gets all the information from the profiles of the winners
    def lookAtWinnerProfiles(self):
        self.fetchMode = "Second"
        print('\nLogging in...\n')
        self.loginToFreelancer()
        # self.winnerProfiles = list(self.profilesSavedAlready.keys())
        for i in range(len(self.winnerProfiles)):
            print("\nProfile " + str(i + 1) + " / " + str(len(self.winnerProfiles)) + ":")
            profileLink = self.winnerProfiles[i]
            print(profileLink)
            self.numOn = i + 1
            if profileLink != "https://www.freelancer.co.uk/u/chukuaile1":
                check = (self.profilesSavedAlready.get(profileLink) is None)
                if check:
                    self.getInformationFromBidderProfile(profileLink)
                    self.profilesSavedAlready.update({profileLink: True})
            # if (self.profilesSavedAlready.get(profileLink) is None):
            #     self.getInformationFromBidderProfile(profileLink)
            #     self.profilesSavedAlready.update({profileLink: True})

    # Creates the Winners table in the database, which will initially be empty
    def createWinnersTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Winners')
        cur.execute('''CREATE TABLE Winners (
        'JobID' INTEGER PRIMARY KEY,
        'JobURL' TEXT NOT NULL,
        'Username' TEXT NOT NULL,
        'ProfileURL' TEXT NOT NULL,
        FOREIGN KEY (JobID) REFERENCES Jobs(JobID)
        );''')

        con.commit()

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
        'ProjectURL' TEXT NOT NULL,
        'Tags' TEXT NOT NULL,
        'Profile' TEXT NOT NULL,
        'Score' INTEGER NOT NULL,
        'AmountPaid' TEXT NOT NULL,
        'Currency' TEXT NOT NULL,
        'ConvertedCurrency' TEXT NOT NULL,
        'DateScraped' TEXT NOT NULL,
        'Date' TEXT NOT NULL,
        'Country' TEXT NOT NULL,
        'Notes' TEXT NOT NULL,
        'DateRange' TEXT,
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
        'Title' TEXT NOT NULL,
        'Description' TEXT NOT NULL,
        'Tags' TEXT NOT NULL,
        'NumberOfBidders' INTEGER NOT NULL,
        'AverageBidCost' TEXT NOT NULL,
        'FinalCost' TEXT NOT NULL,
        'Currency' TEXT NOT NULL,
        'Time' TEXT NOT NULL,
        'ConvertedFinalCost' TEXT NOT NULL,
        'CountryOfPoster' TEXT NOT NULL,
        'CountryOfWinner' TEXT NOT NULL,
        'Year' INTEGER NOT NULL,
        'Week' INTEGER NOT NULL,
        'DateRange' TEXT,
        'Category' INTEGER,
        'Score' INTEGER,
        'PositiveMatches' TEXT,
        'NegativeMatches' TEXT,
        'Attachment' INTEGER,
        'CategoryTypeTwo' INTEGER
        );''')

        con.commit()

    # Creates the JobsHourly table in the database, which will initially be empty
    def createJobsHourlyTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS JobsHourly')
        cur.execute('''CREATE TABLE JobsHourly (
        'JobID' INTEGER PRIMARY KEY,
        'URL' TEXT NOT NULL,
        'Title' TEXT NOT NULL,
        'Description' TEXT NOT NULL,
        'Tags' TEXT NOT NULL,
        'NumberOfBidders' INTEGER NOT NULL,
        'AverageBidCost' TEXT NOT NULL,
        'FinalCost' TEXT NOT NULL,
        'Currency' TEXT NOT NULL,
        'Time' TEXT NOT NULL,
        'ConvertedFinalCost' TEXT NOT NULL,
        'CountryOfPoster' TEXT NOT NULL,
        'CountryOfWinner' TEXT NOT NULL,
        'Year' INTEGER NOT NULL,
        'Week' INTEGER NOT NULL,
        'DateRange' TEXT,
        'Category' INTEGER,
        'Score' INTEGER,
        'PositiveMatches' TEXT,
        'NegativeMatches' TEXT,
        'Attachment' INTEGER
        );''')

        con.commit()

    # Creates the RelevantJobs table in the database, which will initially be empty
    # def createRelevantJobsTable(self):
    #     dbName = "JobDetails.db"
    #     con = lite.connect(dbName)
    #     cur = con.cursor()
    #
    #     cur.execute('DROP TABLE IF EXISTS RelevantJobs')
    #     cur.execute('''CREATE TABLE RelevantJobs (
    #     'JobID' INTEGER PRIMARY KEY,
    #     'URL' TEXT NOT NULL,
    #     'Title' TEXT NOT NULL,
    #     'Description' TEXT NOT NULL,
    #     'Tags' TEXT NOT NULL,
    #     'NumberOfBidders' INTEGER NOT NULL,
    #     'AverageBidCost' TEXT NOT NULL,
    #     'FinalCost' TEXT NOT NULL,
    #     'Currency' TEXT NOT NULL,
    #     'Time' TEXT NOT NULL,
    #     'ConvertedFinalCost' TEXT NOT NULL,
    #     'CountryOfPoster' TEXT NOT NULL,
    #     'CountryOfWinner' TEXT NOT NULL,
    #     'Year' INTEGER NOT NULL,
    #     'Week' INTEGER NOT NULL
    #     );''')
    #
    #     con.commit()

    # Creates the Jobs table in the database, which will initially be empty
    def createReviewJobsTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS ReviewJobs')
        cur.execute('''CREATE TABLE ReviewJobs (
        'JobID' INTEGER PRIMARY KEY,
        'URL' TEXT NOT NULL,
        'Title' TEXT NOT NULL,
        'Description' TEXT NOT NULL,
        'Tags' TEXT NOT NULL,
        'NumberOfBidders' INTEGER NOT NULL,
        'AverageBidCost' TEXT NOT NULL,
        'FinalCost' TEXT NOT NULL,
        'Currency' TEXT NOT NULL,
        'Time' TEXT NOT NULL,
        'ConvertedFinalCost' TEXT NOT NULL,
        'CountryOfPoster' TEXT NOT NULL,
        'CountryOfWinner' TEXT NOT NULL,
        'DateScraped' INTEGER NOT NULL,
        'TimeAgo' INTEGER NOT NULL,
        'DateRange' TEXT,
        'Category' INTEGER,
        'Score' INTEGER,
        'PositiveMatches' TEXT,
        'NegativeMatches' TEXT,
        'Attachment' INTEGER,
        'PossibleYears' TEXT,
        'CategoryTypeTwo' INTEGER
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

    # Creates the Bids table in the database, which will initially be empty
    def createBidsTable(self):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS Bids')
        cur.execute('''CREATE TABLE Bids (
        'BidID' INTEGER PRIMARY KEY,
        'JobID' INTEGER NOT NULL,
        'Country' TEXT NOT NULL,
        'User' TEXT NOT NULL,
        'Price' TEXT NOT NULL,
        'Currency' TEXT NOT NULL
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

        # Checks if tables exist and creates them if they do not
        # cur.execute(
        #     "SELECT name FROM sqlite_master WHERE type='table' AND name='RelevantJobs'")
        # if (len(cur.fetchall()) == 0):
        #     self.createRelevantJobsTable()

        # Checks if tables exist and creates them if they do not
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='ReviewJobs'")
        if (len(cur.fetchall()) == 0):
            self.createReviewJobsTable()

        # Checks if tables exist and creates them if they do not
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='JobsHourly'")
        if (len(cur.fetchall()) == 0):
            self.createJobsHourlyTable()

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

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Bids'")
        if (len(cur.fetchall()) == 0):
            self.createBidsTable()

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Winners'")
        if (len(cur.fetchall()) == 0):
            self.createWinnersTable()

        for table in ["Jobs", "ReviewJobs"]:
            query = "SELECT JobID, AverageBidCost, FinalCost, ConvertedFinalCost FROM " + table
            cur.execute(query)
            res = [list(each) for each in cur.fetchall()]
            for result in res:
                jID = result[0]
                av = result[1]
                if av != "None" and av != "Not Found":
                    av = '{0:.2f}'.format(float(''.join(c for c in av if c.isnumeric() or c == '.')))

                final = result[2]
                if final != "None":
                    final = '{0:.2f}'.format(float(''.join(c for c in final if c.isnumeric() or c == '.')))

                converted = result[2]
                if converted != "None":
                    converted = '{0:.2f}'.format(float(''.join(c for c in converted if c.isnumeric() or c == '.')))

                query = "UPDATE " + table + " SET AverageBidCost = '" + av + "', FinalCost = '" + final + "', ConvertedFinalCost = '" + converted + "' WHERE JobID = " + str(
                    jID)
                cur.execute(query)
                con.commit()

        cur.execute('''SELECT DISTINCT(Country) FROM Bids WHERE Country LIKE "%'%"''')
        res = [[''.join(each[0].split("'")), each[0]] for each in cur.fetchall()]

        for each in res:
            query = '''UPDATE Bids SET Country = "''' + each[0] + '''" WHERE Country = "''' + each[1] + '''"'''
            cur.execute(query)

        for table in ["Jobs", "ReviewJobs"]:
            query = '''SELECT DISTINCT(CountryOfWinner) FROM ''' + table + ''' WHERE CountryOfWinner LIKE "%'%"'''
            cur.execute(query)
            res = [[''.join(each[0].split("'")), each[0]] for each in cur.fetchall()]

            for each in res:
                query = '''UPDATE ''' + table + ''' SET CountryOfWinner = "''' + each[
                    0] + '''" WHERE CountryOfWinner = "''' + each[1] + '''"'''
                cur.execute(query)

            query = '''SELECT DISTINCT(CountryOfPoster) FROM ''' + table + ''' WHERE CountryOfPoster LIKE "%'%"'''
            cur.execute(query)
            res = [[''.join(each[0].split("'")), each[0]] for each in cur.fetchall()]

            for each in res:
                query = '''UPDATE ''' + table + ''' SET CountryOfPoster = "''' + each[
                    0] + '''" WHERE CountryOfPoster = "''' + each[1] + '''"'''
                cur.execute(query)

        con.commit()

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

    # Will save bid details to the database
    def saveBidDetails(self, jobID, country, user, price):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        split = price.text.rstrip().split()

        cur.execute('''
        INSERT INTO Bids(JobID, Country, User, Price, Currency)
        VALUES(?,?,?,?,?)''',
                    (jobID, country, user, split[0], split[1]))

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

        tagString = ""
        for i in range(len(self.tags) - 1):
            tag = self.tags[i]
            tagString += tag + ", "

        if len(self.tags) > 0:
            tagString += self.tags[-1]
        else:
            tagString = "None given"

        if (self.convertedCurrency == -1):
            self.convertedCurrency = "None"

        cur.execute('''
        INSERT INTO Reviews(Profile, ProjectURL, Tags, Score, AmountPaid, Currency, ConvertedCurrency, 
        DateScraped, Date, Country, Notes) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                    (
                        self.username, self.projectLink, tagString, self.score, self.amountPaid, self.currency,
                        self.convertedCurrency,
                        self.dateToday,
                        self.timePosted, self.reviewCountry, self.note))

        con.commit()

    # Will save job details to the database
    def saveJobDetails(self, url):

        if (not (self.awarded)):
            self.winnerCountry = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        if self.numFreelancers == "Other":
            self.numFreelancers = 0

        if (self.numFreelancers == 0):
            self.averagePrice = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        try:
            cur.execute('''
            INSERT INTO Jobs(JobID, URL, Title, Description, Tags, NumberOfBidders, AverageBidCost, FinalCost,
            Currency, Time, ConvertedFinalCost, CountryOfPoster, CountryOfWinner, Year, Week) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (self.projectID, url, self.projectTitle, self.projectDescription, self.tagsToSave,
                         self.numFreelancers,
                         self.averagePrice, self.priceAmount, self.currency, self.time, self.convertedPrice,
                         self.customerCountry, self.winnerCountry, self.year, self.week))

            con.commit()
        except lite.IntegrityError:
            b = 1

    # Will save job details to the database
    def saveJobHourlyDetails(self, url):

        if (not (self.awarded)):
            self.winnerCountry = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        if self.numFreelancers == "Other":
            self.numFreelancers = 0

        if (self.numFreelancers == 0):
            self.averagePrice = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        try:
            cur.execute('''
            INSERT INTO JobsHourly(JobID, URL, Title, Description, Tags, NumberOfBidders, AverageBidCost, FinalCost,
            Currency, Time, ConvertedFinalCost, CountryOfPoster, CountryOfWinner, Year, Week) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (self.projectID, url, self.projectTitle, self.projectDescription, self.tagsToSave,
                         self.numFreelancers,
                         self.averagePrice, self.priceAmount, self.currency, self.time, self.convertedPrice,
                         self.customerCountry, self.winnerCountry, self.year, self.week))

            con.commit()
        except lite.IntegrityError:
            b = 1

    def saveReviewJobDetails(self, url, scraped, timeFrame):
        if (not (self.awarded)):
            self.winnerCountry = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        if self.numFreelancers == "Other":
            self.numFreelancers = 0

        if (self.numFreelancers == 0):
            self.averagePrice = "None"
            self.priceAmount = "None"
            self.convertedPrice = "None"

        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        try:
            cur.execute('''
            INSERT INTO ReviewJobs(JobID, URL, Title, Description, Tags, NumberOfBidders, AverageBidCost, FinalCost,
            Currency, Time, ConvertedFinalCost, CountryOfPoster, CountryOfWinner, DateScraped, TimeAgo) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (self.projectID, url, self.projectTitle, self.projectDescription, self.tagsToSave,
                         self.numFreelancers,
                         self.averagePrice, self.priceAmount, self.currency, self.time, self.convertedPrice,
                         self.customerCountry, self.winnerCountry, scraped, timeFrame))

            con.commit()
        except lite.IntegrityError:
            b = 1

    # Will save winner details to the database
    def saveWinnerDetails(self, jobID, url, user):
        dbName = "JobDetails.db"
        con = lite.connect(dbName)
        cur = con.cursor()

        profileURL = LINK_PREFIX + "/u/" + user

        cur.execute('''
        INSERT INTO Winners(JobID, JobURL, Username, ProfileURL) 
        VALUES(?,?,?,?)''',
                    (jobID, url, user, profileURL))

        con.commit()

    # Closes the window
    def exit(self):
        main.close()

    # Fetching all the data that requires a login first
    def fetchDataWithLogin(self):
        profileLinks = list(self.profilesSeen.keys())[:2]
        for profile in profileLinks:
            self.getInformationFromBidderProfile(profile)

    # Fetching all the data that we need without logging in
    def fetchDataNonLogin(self, url, data):
        print("\n" + url)
        if (len(url.split('/')) == 7):
            r = requests.get(url)
            self.soup = BeautifulSoup(r.content, "html.parser")

            try:
                self.projectID = self.soup.find_all(
                    "p", {"class": "PageProjectViewLogout-detail-tags"}
                )[-1].text.split("#")[-1]
            except IndexError:
                self.projectID = -1

            if (self.seenIDs.get(self.projectID) == None) and (self.projectID != -1):

                self.seenIDs[self.projectID] = True

                try:
                    self.projectTitle = self.soup.find(
                        "h1", {"class": "PageProjectViewLogout-header-title"}).text

                    go = True
                except AttributeError:
                    go = False

                if go:

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

                    # self.awarded = False

                    # Retrieving the final price for the task if we are looking at
                    # a completed project in the archives
                    self.finalPrice = ""

                    try:
                        check = self.biddersAndPriceFind.find("span",
                                                              {"class": "PageProjectViewLogout-awardedTo-heading"}).text
                        self.awarded = True
                    except AttributeError:
                        self.awarded = False

                    # Retrieving the final price for the task if we are looking at
                    # a completed project in the archives
                    try:
                        self.finalPrice = self.soup.find(
                            "div", {"class": "FreelancerInfo-price"}).text
                        yes = True
                    except AttributeError:
                        self.finalPrice = self.soup.find(
                            "p", {"class": "PageProjectViewLogout-header-byLine"}).text
                        yes = False

                    split = self.finalPrice.split()
                    self.priceAmount = "None"
                    if yes:
                        self.priceAmount = split[0]
                    self.currency = split[1]

                    # Checks if the project was awarded to anyone
                    if (self.archived and self.awarded):
                        # self.awarded = True

                        # Makes sure the bidding info is correct as archived pages use
                        # a slightly different format
                        self.biddersAndPriceFind = self.biddersInfo[1]

                        # self.winner = LINK_PREFIX + self.soup.find(
                        #     "a", {"class": "FreelancerInfo-username"}).get("href")
                        self.winnerCountry = self.soup.find(
                            "span", {"class": "usercard-flag"}).get("title")

                        self.finalPrices.append(self.finalPrice)

                        try:
                            self.time = split[3] + " " + split[4]
                        except IndexError:
                            a = 1

                    self.projectDescription = ""
                    descriptionTags = self.soup.find_all("p", {"class": "PageProjectViewLogout-detail-paragraph"})

                    for item in descriptionTags:
                        self.projectDescription += item.text

                    # Retrieving the tags that the customer gave to their task
                    self.givenTags = self.soup.find_all(
                        "a", {"class": "PageProjectViewLogout-detail-tags-link--highlight"})

                    self.tagsToSave = ""
                    for i in range(len(self.givenTags) - 1):
                        self.tagsToSave += self.givenTags[i].text + ", "

                    self.tagsToSave += self.givenTags[-1].text

                    # Get the country of the customer
                    self.getCustomerCountry()

                    # Gets the information about the bidders
                    self.getBiddersInfo(url)

                    avPriceCheck = self.averagePrice.split("/hour")[0]

                    if data != []:
                        self.saveReviewJobDetails(url, data[0], data[1])
                    else:
                        if (avPriceCheck == self.averagePrice):
                            self.saveJobDetails(url)
                        else:
                            self.averagePrice = avPriceCheck
                            self.saveJobHourlyDetails(url)

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
    def getBiddersInfo(self, url):
        # A list for the links to the bidders' profiles
        self.bidderProfileLinks = []

        # Adding each link to the bidder profiles to the list
        bidderLinks = self.soup.find_all(
            "a", {"class": "FreelancerInfo-username"})

        self.users = [link.text for link in bidderLinks]

        for each in bidderLinks:
            self.bidderProfileLinks.append(LINK_PREFIX + each.get("href"))

        self.numFreelancers = 0
        self.averagePrice = ""

        # Check if anyone has bid on the job yet
        if (self.biddersAndPriceFind.text.split("Need to")
        [0] == self.biddersAndPriceFind.text):
            division = self.biddersAndPriceFind.text.split(" ")

            self.numFreelancers = division[0]
            self.averagePrice = ""
            # self.averagePrice = division[6]
            # print(
            #     self.numFreelancers +
            #     " freelancers who are bidding an average of " +
            #     self.averagePrice)

            currencySplit = self.finalPrice.split()

            if (self.awarded):
                print("The final price was: " + self.finalPrice + "\n")
                winnerProfile = LINK_PREFIX + bidderLinks[0].get("href")
                if (self.fetchMode == "First"):
                    self.winnerProfiles.append(winnerProfile)
                currency = currencySplit[1]
                amount = ''.join(c for c in currencySplit[0] if c.isalnum())
                # self.convertedPrice = "$" + convertCurrencyWithYear(currency, amount, self.week, self.year)
                self.saveWinnerDetails(self.projectID, url, self.users[0])

            else:
                # self.currency = self.soup.find("p", {"class": "PageProjectViewLogout-header-byLine"}).text.split()[-1]
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

        prices = self.soup.find_all("div", {"class": "FreelancerInfo-price"})

        # Saving the locations of bidders and the number from that country into
        # the dictionary
        for i in range(len(self.bidderCountries)):
            location = self.bidderCountries[i]
            # Gets the country of the bidder
            country = location.contents[1].get("title")
            if (country == "Palestinian Territory"):
                country = "Palestine"

            num = 1

            # Checks if the country is already in the dictionary
            result = self.countriesOfBidders.get(country)

            # Incrementing value if country already in dictionary
            if (result is not None):
                num = result + 1

            if ((i == 0) and (self.awarded)):
                winnerNum = 1

                # Checks if the country is already in the dictionary
                winnerResult = self.winnerCountries.get(country)

                # Incrementing value if country already in dictionary
                if (winnerResult is not None):
                    winnerNum = winnerResult + 1

                self.winnerCountries.update({country: num})

            # Updating the dictionary with the country data
            self.countriesOfBidders.update({country: num})
            self.saveBidDetails(self.projectID, country, self.users[i], prices[i])

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

        b = 1
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
            try:
                name = qual.find_element_by_class_name("skill-exam-link").text
                score = qual.find_element_by_class_name("skill-exam-value").text
                self.certsDict[name] = score
            except NoSuchElementException:
                g = 1

    # Retrieves details on the reviews on the given bidder profile
    def getReviewDetails(self):
        numDiscounted = 0

        # Expand to get all reviews
        self.driver.find_element(
            By.CLASS_NAME,
            "profile-reviews-btn-top").click()

        time.sleep(3)

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

        con = lite.connect(DATABASE_NAME)
        cur = con.cursor()
        cur.execute('SELECT COUNT(*) From (SELECT Profile FROM Reviews WHERE Profile = ?) AS result',
                    [self.username])

        numFound = int(cur.fetchall()[0][0])

        if numFound == self.numReviews:
            done = True
        else:
            done = False
            self.startFrom = numFound

        page = 0

        links = {}
        duplicates = 0

        dupes = []

        pageNeeded = math.floor(self.startFrom / 100)
        first = True

        while page < pageNeeded:
            pageButtons = self.driver.find_element_by_class_name(
                "user-reviews-pagination")
            page += 1
            nextPageButton = pageButtons.find_elements_by_tag_name(
                "li")[-2]
            nextPageButton.find_element_by_tag_name("a").click()
            time.sleep(1.5)

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

            if first:
                i = (self.startFrom % 100)
            else:
                i = 0

            if (page == math.floor(self.numReviews / 100)):
                if first:
                    reviews = reviews[:(len(reviews) - self.startFrom)]
                else:
                    reviews = reviews[:(self.numReviews % 100)]

            # Go through all the reviews on the current page
            while i < (len(reviews)):
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

                testValue = amountElement.find_elements_by_css_selector(
                    "span[ng-show='review.get().paid_amount !== 0']")

                value = amountElement.find_element_by_class_name(
                    "ng-binding").text
                self.amountPaid = value + " " + amountElement.text
                splitThing = self.amountPaid.split()

                if (len(self.amountPaid.split()) != 2):
                    self.amountPaid = amountElement.text
                try:
                    self.currency = self.amountPaid.split()[1]
                    self.amountPaid = self.amountPaid.split()[0]
                except IndexError:
                    # sib = amountElement.get_attribute("nextSibling")
                    # self.currency = sib.get_attribute("data").rstrip()
                    amount = amountElement.get_attribute("innerText")
                    split = amount.split()
                    self.currency = split[-1]
                    self.amountPaid = "SEALED"

                self.reviewCountry = review.find_element_by_class_name("user-review-flag").get_attribute("title")
                self.timePosted = ' '.join(review.find_element_by_class_name("user-review-details").text.split(".")[
                                               -2].lstrip().split()[-3:])

                self.convertedCurrency = -1

                tagList = review.find_element_by_class_name("user-rating-skills")
                self.tags = []

                tagItems = tagList.find_elements_by_tag_name("li")

                for tag in tagItems:
                    self.tags.append(tag.text)

                if (self.amountPaid == " "):
                    countReview = False
                    sealed = True
                else:
                    timeSplit = self.timePosted.split()
                    timeFrame = timeSplit[1]
                    timeAmount = int(timeSplit[0])
                    self.convertedCurrency = ""
                    if (self.amountPaid != "SEALED"):
                        valuePaid = float(''.join(c for c in self.amountPaid if c.isnumeric() or c == '.'))

                    # if ((timeFrame == 'month') or (timeFrame == 'months')):
                    #     self.convertedCurrency = calculateMonthlyAverage(self.currency, valuePaid, timeAmount)
                    # elif ((timeFrame == 'week') or (timeFrame == 'weeks')):
                    #     self.convertedCurrency = calculateWeeklyAverage(self.currency, valuePaid, timeAmount)
                    # elif ((timeFrame == 'year') or (timeFrame == 'years')):
                    #     self.convertedCurrency = calculateYearlyAverage(self.currency, valuePaid,
                    #                                                     date.today().year - timeAmount)
                    # elif ((timeFrame == 'day') or (timeFrame == 'days')):
                    #     dateToConvert = date.today() - relativedelta(days=timeAmount)
                    #     self.convertedCurrency = convertCurrency(self.currency, valuePaid, dateToConvert)

                # Gets the review text
                reviewText = review.find_element_by_tag_name(
                    "p").text.split('"')[1:][:-1][0]

                titleFind = review.find_element_by_class_name(
                    "user-review-title")

                # Gets the link to the project that the review is for
                self.projectLink = titleFind.get_attribute("href")

                self.reviewTitle = titleFind.text

                if (links.get(self.projectLink) is None):
                    if (self.reviewTitle.split("Project for")[0] == self.reviewTitle and
                            self.reviewTitle.split("deleted")[0] == self.reviewTitle):
                        links[self.projectLink] = [self.dateToday, self.timePosted]
                        if (self.projectsSavedAlready.get(self.projectLink) is None):
                            self.fetchDataNonLogin(self.projectLink, links.get(self.projectLink))
                else:
                    duplicate = True

                # Temporary output of the extracted data
                print("Profile " + str(self.numOn) + " / " + str(len(self.winnerProfiles)) + " - Review " + str(
                    i + 1 + (page * 100)) +
                      " / " + str(self.numReviewsToOutput))

                saveReview = True

                self.note = "None"
                i += 1
                if first == True:
                    first = False

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

                # for link in links.keys():
                #     if (self.projectsSavedAlready.get(link) is None):
                #         self.fetchDataNonLogin(link, links.get(link))

                # for project in (list(links.keys())):
                #     if self.projectsSeen.get(project) is None:
                #         self.projectsSeen[project] = True

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


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
app.exec()
