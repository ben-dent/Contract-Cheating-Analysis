import sqlite3 as lite
import sys

from PyQt5 import uic, QtWidgets

DATABASE_NAME = 'JobDetails.db'

categoriseUi = uic.loadUiType('UIs/categoriseUI.ui')[0]


class Categorise(QtWidgets.QMainWindow, categoriseUi):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.chosen = -1
        self.currentList = "Jobs"
        self.i = 0

        self.cats = []

        self.btn1.clicked.connect(self.one)
        self.btn2.clicked.connect(self.two)
        self.btn3.clicked.connect(self.three)
        self.btn4.clicked.connect(self.four)
        self.btn5.clicked.connect(self.five)

        self.con = lite.connect(DATABASE_NAME)
        self.cur = self.con.cursor()

        self.getData()
        print(len(self.jobData))
        print(len(self.reviewJobData))

        if (self.currentList == "Jobs"):
            l = self.jobData
        else:
            l = self.reviewJobData

        self.display(l, 0)

    def display(self, l, i):
        self.close()
        job = l[i]
        self.jID = job[0]
        title = job[1] + " - Job " + str(i + 1) + " / " + str(self.numProjects)
        tags = job[2]
        description = job[3]


        self.lblTitle.setText(title)
        self.lblTags.setText(tags)
        self.txtDescription.setPlainText(description)
        self.show()

    def getData(self):
        self.cur.execute('SELECT JobID, Title, Tags, Description FROM Jobs WHERE Category = -1 OR Category IS NULL')
        self.jobData = [list(each) for each in self.cur.fetchall()]

        self.cur.execute('SELECT COUNT(JobID) FROM Jobs WHERE Category = -1 OR Category IS NULL')

        tot1 = int(self.cur.fetchall()[0][0])

        if (tot1 == 0):
            self.currentList = "ReviewJobs"

        self.cur.execute('SELECT JobID, Title, Tags, Description FROM ReviewJobs WHERE Category = -1 OR Category IS NULL')
        self.reviewJobData = [list(each) for each in self.cur.fetchall()]

        self.cur.execute('SELECT COUNT(JobID) FROM ReviewJobs WHERE Category = -1 OR Category IS NULL')

        self.numProjects = tot1 + int(self.cur.fetchall()[0][0])

    def displayNext(self):
        self.saveCategory()
        self.i += 1
        if (self.currentList == "Jobs"):
            if (self.i < len(self.jobData)):
                self.display(self.jobData, self.i)
            else:
                self.currentList = "ReviewJobs"
                self.i = 0
                self.display(self.reviewJobData, 0)

        else:
            if (self.i < len(self.reviewJobData)):
                self.display(self.reviewJobData, self.i)
            else:
                self.close()
                # self.saveCategories()

    def saveCategory(self):
        j = self.cats[-1]
        cat = j[1]
        job = j[0]
        query = "UPDATE " + self.currentList + " SET Category = " + str(cat) + " WHERE JobID = " + str(job)
        self.cur.execute(query)

        self.con.commit()


    def saveCategories(self):
        for pair in self.cats:
            job = pair[0]
            cat = pair[1]
            query = "UPDATE " + self.currentList + " SET Category = " + str(cat) + " WHERE JobID = " + str(job)
            self.cur.execute(query)

        self.con.commit()

    def one(self):
        self.cats.append([self.jID, 1])
        self.displayNext()

    def two(self):
        self.cats.append([self.jID, 2])
        self.displayNext()

    def three(self):
        self.cats.append([self.jID, 3])
        self.displayNext()

    def four(self):
        self.cats.append([self.jID, 4])
        self.displayNext()

    def five(self):
        self.cats.append([self.jID, 5])
        self.displayNext()


app = QtWidgets.QApplication(sys.argv)
c = Categorise()
c.show()
app.exec()
