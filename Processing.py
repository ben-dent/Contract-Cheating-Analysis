import sys

from PyQt5 import uic, QtWidgets

from DataAnalysis import *

uiFolder = "UIs/"


def getUI(name):
    return uic.loadUiType(uiFolder + name + ".ui")[0]


processingUi = getUI("processingUI")
countryUi = getUI("countryUI")
tagUi = getUI("tagUI")
categoryUi = getUI("categoryUI")
dateRangeUi = getUI("dateRangeUI")
keywordUi = getUI("keywordUI")
statsUi = getUI('viewStats')
trendsUi = getUI('trends')
plotYearUi = getUI('plotByYear')


class Processing(QtWidgets.QMainWindow, processingUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnCountryBids.clicked.connect(self.countryBids)
        self.btnCountryPosters.clicked.connect(self.countryPosters)
        self.btnCountryWinners.clicked.connect(self.countryWinners)
        self.btnTag.clicked.connect(self.tag)
        self.btnCategory.clicked.connect(self.category)
        self.btnDateRange.clicked.connect(self.dateRange)
        self.btnKeyword.clicked.connect(self.keyword)
        self.btnViewStats.clicked.connect(self.viewStats)

    def countryBids(self):
        l.processing.close()
        l.launchCountryBids()

    def countryPosters(self):
        l.processing.close()
        l.launchCountryPosters()

    def countryWinners(self):
        l.processing.close()
        l.launchCountryWinners()

    def tag(self):
        l.processing.close()
        l.launchTag()

    def category(self):
        l.processing.close()
        l.launchCategory()

    def dateRange(self):
        l.processing.close()
        l.launchDateRange()

    def keyword(self):
        l.processing.close()
        l.launchKeyword()

    def viewStats(self):
        l.processing.close()
        l.launchViewStats()


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

            l.cur.execute(
                'SELECT DISTINCT(CountryOfPoster) FROM ReviewJobs WHERE CountryOfPoster NOT IN (SELECT CountryOfPoster FROM Jobs)')
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


class Tag(QtWidgets.QMainWindow, tagUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.btnExport.clicked.connect(self.export)
        self.btnBack.clicked.connect(self.back)

        l.cur.execute('SELECT DISTINCT(Tags) FROM Jobs')
        self.categories = set()
        for each in l.cur.fetchall():
            tags = each[0]
            for tag in tags.split(','):
                self.categories.add(tag)

        l.cur.execute('SELECT DISTINCT(Tags) FROM ReviewJobs')
        for each in l.cur.fetchall():
            tags = each[0]
            for tag in tags.split(','):
                self.categories.add(tag)

        self.categories = list(self.categories)
        self.cmbTags.addItems(sorted(self.categories))

    def getFreq(self):
        n = 0
        query = "SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%" + self.tag + "'"
        l.cur.execute(query)

        n += int(l.cur.fetchone()[0])

        query = "SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%" + self.tag + "'"
        l.cur.execute(query)

        n += int(l.cur.fetchone()[0])
        return n

    def export(self):
        if (self.cmbTags.currentIndex() == 0):
            QtWidgets.QMessageBox.warning(self, "Please select a tag!", "Please select a tag!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            category = self.cmbTags.currentText()
            filter = "Tags LIKE '%" + category + "%'"
            file = "Tag - " + category + ".csv"
            saveToCSV(["Jobs", "ReviewJobs"], '*', filter, file)
            QtWidgets.QMessageBox.information(self, "Exported!", "Exported!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.cmbTags.setCurrentIndex(0)

    def back(self):
        l.tag.close()
        l.launchProcessing()


class Category(QtWidgets.QMainWindow, categoryUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnBack.clicked.connect(self.back)
        self.btnGraphAll.clicked.connect(self.graphAll)
        self.btnExport.clicked.connect(self.export)

    def graphAll(self):
        data = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}

        for table in ['Jobs', 'ReviewJobs']:
            for i in range(1, 6):
                query = 'SELECT COUNT(JobID) FROM ' + table + ' WHERE Category = ' + str(i)
                l.cur.execute(query)
                current = data.get(str(i))
                data.update({str(i): current + int(l.cur.fetchone()[0])})

        plotAllCategories(data)

    def getFreq(self):
        n = 0
        query = "SELECT COUNT(JobID) FROM Jobs WHERE Category = " + str(self.category)
        l.cur.execute(query)

        n += int(l.cur.fetchone()[0])

        query = "SELECT COUNT(JobID) FROM ReviewJobs WHERE Category = " + str(self.category)
        l.cur.execute(query)

        n += int(l.cur.fetchone()[0])
        return n

    def export(self):
        valid = False
        val = self.cmbCategories.currentIndex()

        if (val == 0):
            QtWidgets.QMessageBox.warning(self, "Please select a category!", "Please select a category!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            valid = True

        if valid:
            filter = "Category = " + str(val)
            file = "Category - " + str(val) + ".csv"
            saveToCSV(["Jobs", "ReviewJobs"], '*', filter, file)
            QtWidgets.QMessageBox.information(self, "Exported!", "Exported!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.cmbCategories.setCurrentIndex(0)

    def back(self):
        l.category.close()
        l.launchProcessing()


class DateRange(QtWidgets.QMainWindow, dateRangeUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnBack.clicked.connect(self.back)
        self.btnExport.clicked.connect(self.export)

    def checkValid(self):
        validStart = False
        validEnd = False

        start = self.edtStartDate.text()
        end = self.edtEndDate.text()

        startSplit = start.split("/")

        if (len(startSplit) == 3):
            parts = []
            for part in startSplit:
                try:
                    int(part)
                    parts.append(True)
                except ValueError:
                    parts.append(False)

            if False not in parts:
                validStart = True

        if not validStart:
            QtWidgets.QMessageBox.warning(self, "Enter valid start date!", "Enter valid start date!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return False

        endSplit = end.split("/")

        if (len(endSplit) == 3):
            parts = []
            for part in endSplit:
                try:
                    int(part)
                    parts.append(True)
                except ValueError:
                    parts.append(False)

            if False not in parts:

                startSplit = [int(each) for each in startSplit]
                endSplit = [int(each) for each in endSplit]

                startDate = date(startSplit[2], startSplit[1], startSplit[0])
                endDate = date(endSplit[2], endSplit[1], endSplit[0])

                if endDate >= startDate:
                    validEnd = True

        if not validEnd:
            QtWidgets.QMessageBox.warning(self, "Enter valid end date!", "Enter valid end date!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return False

        return True

    def export(self):
        valid = self.checkValid()
        if valid:
            start = self.edtStartDate.text()
            end = self.edtEndDate.text()
            saveDateRange(start, end)
            QtWidgets.QMessageBox.information(self, "Exported!", "Exported!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.edtStartDate.setText("")
            self.edtEndDate.setText("")

    def back(self):
        l.dateRange.close()
        l.launchProcessing()


class Keyword(QtWidgets.QMainWindow, keywordUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnExport.clicked.connect(self.export)
        self.btnBack.clicked.connect(self.back)

    def checkValid(self):
        keyword = self.edtKeyword.text()

        if (keyword == ""):
            QtWidgets.QMessageBox.warning(self, "Please enter a keyword!", "Please enter a keyword!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return False
        else:
            return True

    def export(self):
        valid = self.checkValid()

        keyword = self.edtKeyword.text()

        if valid:
            keywordFilter = "'%" + keyword + "'"
            filter = "(Title LIKE " + keywordFilter + ") OR (Description LIKE " + keywordFilter + ") OR Tags LIKE " + keywordFilter + ")"

            sum = 0

            for table in ["Jobs", "ReviewJobs"]:
                query = "SELECT COUNT(JobID) FROM " + table + " WHERE " + filter
                l.cur.execute(query)
                sum += int(l.cur.fetchone()[0])

            if (sum > 0):
                file = "Keyword - " + keyword + ".csv"
                saveToCSV(["Jobs", "ReviewJobs"], '*', filter, file)
                QtWidgets.QMessageBox.information(self, "Exported!", "Exported!",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

            else:
                QtWidgets.QMessageBox.warning(self, "No results found!", "No results found!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

            self.edtKeyword.setText("")

    def back(self):
        l.keyword.close()
        l.launchProcessing()


class ViewStats(QtWidgets.QMainWindow, statsUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.setLabels()

        self.btnBack.clicked.connect(self.back)

        self.btnGetTrends.clicked.connect(self.getTrends)

    def setLabels(self):
        numJobs = 0
        l.cur.execute('SELECT COUNT(JobID) FROM Jobs')
        numJobs += l.cur.fetchone()[0]

        l.cur.execute('SELECT COUNT(JobID) FROM ReviewJobs')
        numJobs += l.cur.fetchone()[0]

        numCategorised = 0

        l.cur.execute("SELECT COUNT(JobID) FROM Jobs WHERE Category IS NOT NULL AND Category != 'None'")
        numCategorised += l.cur.fetchone()[0]

        l.cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE Category IS NOT NULL AND Category != 'None'")
        numCategorised += l.cur.fetchone()[0]

        numPlagiarism = 0

        l.cur.execute('SELECT COUNT(JobID) FROM Jobs WHERE Category = 4 OR Category = 5')
        numPlagiarism += l.cur.fetchone()[0]

        l.cur.execute('SELECT COUNT(JobID) FROM ReviewJobs WHERE Category = 4 OR Category = 5')
        numPlagiarism += l.cur.fetchone()[0]

        pctCategorised = round((numCategorised / numJobs) * 100, 2)
        pctPlagiarism = round((numPlagiarism / numCategorised) * 100, 2)

        essayNum = 0

        l.cur.execute("SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%'")
        essayNum += l.cur.fetchone()[0]

        l.cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%'")
        essayNum += l.cur.fetchone()[0]

        essayCategorised = 0

        l.cur.execute("SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%' AND Category IS NOT NULL AND Category != 'None'")
        essayCategorised += l.cur.fetchone()[0]

        l.cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%' AND Category IS NOT NULL AND Category != 'None'")
        essayCategorised += l.cur.fetchone()[0]

        pctEssayCategorised = round((essayCategorised / essayNum) * 100, 2)

        essayPlagiarism = 0

        l.cur.execute("SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%' AND (Category = 4 OR Category = 5)")
        essayPlagiarism += l.cur.fetchone()[0]

        l.cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Essay Writing%' AND Tags NOT LIKE '%Academic Writing%' AND (Category = 4 OR Category = 5)")
        essayPlagiarism += l.cur.fetchone()[0]

        pctEssayPlagiarism = round((essayPlagiarism / essayCategorised) * 100, 2)

        academicNum = 0

        l.cur.execute("SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%'")
        academicNum += l.cur.fetchone()[0]

        l.cur.execute("SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%'")
        academicNum += l.cur.fetchone()[0]

        academicCategorised = 0

        l.cur.execute(
            "SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%' AND Category IS NOT NULL AND Category != 'None'")
        academicCategorised += l.cur.fetchone()[0]

        l.cur.execute(
            "SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%' AND Category IS NOT NULL AND Category != 'None'")
        academicCategorised += l.cur.fetchone()[0]

        pctAcademicCategorised = round((academicCategorised / academicNum) * 100, 2)

        academicPlagiarism = 0

        l.cur.execute(
            "SELECT COUNT(JobID) FROM Jobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%' AND (Category = 4 OR Category = 5)")
        academicPlagiarism += l.cur.fetchone()[0]


        l.cur.execute(
            "SELECT COUNT(JobID) FROM ReviewJobs WHERE Tags LIKE '%Academic Writing%' AND Tags NOT LIKE '%Essay Writing%' AND (Category = 4 OR Category = 5)")
        academicPlagiarism += l.cur.fetchone()[0]

        pctAcademicPlagiarism = round((academicPlagiarism / academicCategorised) * 100, 2)

        tagTot = essayCategorised + academicCategorised
        tagPlagiarismTot = essayPlagiarism + academicPlagiarism
        tagPctPlagiarism = round((tagPlagiarismTot / tagTot) * 100, 2)

        self.lblNumProjects.setText('Number of projects: ' + str(numJobs))
        self.lblNumCategorised.setText('Number categorised: ' + str(numCategorised) + " (" + str(pctCategorised) + "%)")
        self.lblNumPlagiarism.setText(
            'Number considered plagiarism: ' + str(numPlagiarism) + " (" + str(pctPlagiarism) + "%)")

        self.lblEssayNum.setText("Number from 'Essay Writing' tag: " + str(essayNum))
        self.lblEssayCategorised.setText('Number categorised: ' + str(essayCategorised) + " (" + str(pctEssayCategorised) + "%)")
        self.lblNumPlagiarismEssay.setText(
            "Number considered plagiarism: " + str(essayPlagiarism) + " (" + str(pctEssayPlagiarism) + "%)")

        self.lblAcademicNum.setText("Number from 'Academic Writing' tag: " + str(academicNum))
        self.lblAcademicCategorised.setText(
            'Number categorised: ' + str(academicCategorised) + " (" + str(pctAcademicCategorised) + "%)")
        self.lblNumPlagiarismAcademic.setText(
            "Number considered plagiarism: " + str(academicPlagiarism) + " (" + str(pctAcademicPlagiarism) + "%)")

        self.lblNumPlagiarismBoth.setText(
            "Plagiarism across both tags: " + str(tagPlagiarismTot) + "/" + str(tagTot) + " (" + str(tagPctPlagiarism) + "%)"
        )

    def getTrends(self):
        l.viewStats.close()
        l.launchTrends()

    def back(self):
        l.viewStats.close()
        l.launchProcessing()


class Trends(QtWidgets.QMainWindow, trendsUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.btnGraphByCountry.clicked.connect(self.plotBidderCountries)
        self.btnGraphByWorkerCountry.clicked.connect(self.plotWorkerCountries)

        self.btnGraphBiddersByYear.clicked.connect(self.plotBiddersByYear)
        self.btnGraphWorkersByYear.clicked.connect(self.plotWorkersByYear)
        self.btnGraphProjectsByYear.clicked.connect(self.plotProjectsByYear)
        self.btnGraphProjectsByCategory.clicked.connect(self.plotProjectsByCategory)

        self.btnNumBiddersTime.clicked.connect(self.plotBiddersOverTime)
        self.btnNumWorkersTime.clicked.connect(self.plotWorkersOverTime)

        self.btnBack.clicked.connect(self.back)

    def plotBiddersOverTime(self):
        return

    def plotWorkersOverTime(self):
        return

    def plotBiddersByYear(self):
        l.trends.close()
        l.launchPlotYearBids()

    def plotWorkersByYear(self):
        l.trends.close()
        l.launchPlotYearWorkers()

    def plotBidderCountries(self):
        data = {}

        l.cur.execute(
            "SELECT DISTINCT(Country) FROM Bids WHERE User IN (SELECT DISTINCT(User) FROM Bids) AND Country != 'None'")

        countries = [each[0] for each in l.cur.fetchall()]

        for country in countries:
            if country != 'None':
                query = "SELECT COUNT(Country) FROM Bids WHERE Country = '" + country + "'"
                l.cur.execute(query)
                num = l.cur.fetchone()[0]
                data.update({country: num})

        plotBarChartsOfBidderCountries(data)

    def plotWorkerCountries(self):
        data = {}

        l.cur.execute('SELECT CountryOfWinner FROM Jobs')

        countries = [each[0] for each in l.cur.fetchall()]

        l.cur.execute('SELECT CountryOfWinner FROM ReviewJobs')

        countries += [each[0] for each in l.cur.fetchall() if each[0] not in countries]

        for country in countries:
            if country != 'None':
                val = data.get(country)
                if val is not None:
                    data.update({country: val + 1})
                else:
                    data.update({country: 1})

        plotBarChartsOfBidderCountries(data)

    def plotProjectsByYear(self):
        startYear = 9999
        endYear = 0

        l.cur.execute('SELECT DateRange FROM Jobs')
        res = l.cur.fetchall()
        for each in res:
            dateRange = each[0]
            split = dateRange.split()

            start = 2000 + int(split[0].split('/')[-1])
            end = 2000 + int(split[-1].split('/')[-1])

            if start < startYear:
                startYear = start

            if end > endYear:
                endYear = start

        data = {}

        for year in range(startYear, endYear + 1):
            query = 'SELECT COUNT(JobID) FROM Jobs WHERE Year = ' + str(year)
            l.cur.execute(query)
            num = l.cur.fetchone()[0]

            start = date(year, 1, 1)
            end = date(year, 12, 31)

            num += len(jobsInDateRange(start, end))

            data.update({year: num})

        plotComparison(data, 'Years')

    def plotProjectsByCategory(self):
        data = {}

        for i in range(1, 6):
            query = 'SELECT COUNT(JobID) FROM Jobs WHERE Category = ' + str(i)
            l.cur.execute(query)
            num = l.cur.fetchone()[0]

            query = 'SELECT COUNT(JobID) FROM ReviewJobs WHERE Category = ' + str(i)
            l.cur.execute(query)
            num += l.cur.fetchone()[0]

            data.update({i: num})

        query = "SELECT COUNT(JobID) FROM Jobs WHERE Category IS NULL OR Category = 'None'"
        l.cur.execute(query)
        num = l.cur.fetchone()[0]

        query = "SELECT COUNT(JobID) FROM ReviewJobs WHERE Category IS NULL OR Category = 'None'"
        l.cur.execute(query)
        num += l.cur.fetchone()[0]

        data.update({"9": num})

        plotComparison(data, 'Categories')

    def back(self):
        l.trends.close()
        l.launchViewStats()


class PlotByYear(QtWidgets.QMainWindow, plotYearUi):
    def __init__(self, type, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.type = type

        self.setWindowTitle('Plot By Year - ' + self.type)
        self.lblTitle.setText('Plot ' + self.type + ' By Year')

        self.btnPlot.clicked.connect(self.plot)
        self.btnBack.clicked.connect(self.back)

    def plot(self):
        entered = self.edtYear.text()
        enteredYear = (len(entered) > 0)
        validYear = False

        if not enteredYear:
            QtWidgets.QMessageBox.warning(self, 'Enter year!', 'Enter year!',
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        else:
            try:
                year = int(enteredYear)
                validYear = True
            except ValueError:
                validYear = False

            if validYear:
                year = int(entered)

                start = date(year, 1, 1)
                end = date(year, 12, 31)

                data = {}

                countries = []

                jobData = jobsInDateRange(start, end)

                if (self.type == 'Workers'):
                    countries = [each[1] for each in jobData if each[1] != 'None']
                else:
                    for job in jobData:
                        jID = job[0]
                        query = 'SELECT Country FROM Bids WHERE JobID = ' + str(jID)
                        l.cur.execute(query)
                        countries += [each[0] for each in l.cur.fetchall()]

                for country in countries:
                    if country != 'None':
                        val = data.get(country)
                        if val is not None:
                            data.update({country: val + 1})
                        else:
                            data.update({country: 1})

                plotBarChartsOfBidderCountries(data)


            else:
                QtWidgets.QMessageBox.warning(self, 'Enter valid year!', 'Enter valid year!',
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def back(self):
        l.plotYear.close()
        l.launchTrends()

    def keyPressEvent(self, event):
        ENTER_KEY = 16777220
        if (event.key() == ENTER_KEY):
            self.plot()
        else:
            super().keyPressEvent(event)


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

    def launchTag(self):
        self.tag = Tag()
        self.tag.show()

    def launchCategory(self):
        self.category = Category()
        self.category.show()

    def launchDateRange(self):
        self.dateRange = DateRange()
        self.dateRange.show()

    def launchKeyword(self):
        self.keyword = Keyword()
        self.keyword.show()

    def launchViewStats(self):
        self.viewStats = ViewStats()
        self.viewStats.show()

    def launchTrends(self):
        self.trends = Trends()
        self.trends.show()

    def launchPlotYearBids(self):
        self.plotYear = PlotByYear("Bidders")
        self.plotYear.show()

    def launchPlotYearWorkers(self):
        self.plotYear = PlotByYear("Workers")
        self.plotYear.show()


app = QtWidgets.QApplication(sys.argv)
l = Launcher()
l.launchProcessing()
app.exec()
