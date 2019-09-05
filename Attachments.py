import sqlite3 as lite
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def loginToFreelancer():
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
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(20)

    # Opens the Freelancer login page
    driver.get("https://www.freelancer.co.uk/login")

    # Fills in the username
    userField = driver.find_element_by_id("username")
    userField.send_keys(username)

    # Fills in the password
    passwordField = driver.find_element_by_id("password")
    passwordField.send_keys(password)

    time.sleep(1)

    # Clicks the submit button
    submitButton = driver.find_element_by_id("login_btn")
    submitButton.click()

    time.sleep(4)
    return driver


def getData():
    con = lite.connect('JobDetails.db')
    cur = con.cursor()

    results = []

    for table in ['Jobs', 'ReviewJobs']:
        query = 'SELECT JobID, URL FROM ' + table
        cur.execute(query)
        results += [list(each) for each in cur.fetchall()]

    return results

driver = loginToFreelancer()

data = getData()

res = []

numFound = 0

for i in range(len(data)):
    print('Job ' + str(i + 1) + "/" + str(len(data)))
    each = data[i]
    jID = each[0]
    url = each[1]
    driver.get(url)
    time.sleep(1)

    found = (len(driver.find_elements_by_tag_name('h6')) == 1)

    if found:
        numFound += 1

    res.append([jID, found])

con = lite.connect('JobDetails.db')
cur = con.cursor()

for i in range(len(res)):
    print('Job ' + str(i + 1) + "/" + str(len(res)))
    pair = res[i]
    jID = pair[0]
    found = pair[1]

    if found:
        toWrite = 1
    else:
        toWrite = 0

    query = 'UPDATE Jobs SET Attachment = ' + str(toWrite) + 'WHERE JobID = ' + str(jID)
    cur.execute(query)
    con.commit()

    query = 'UPDATE ReviewJobs SET Attachment = ' + str(toWrite) + 'WHERE JobID = ' + str(jID)
    cur.execute(query)
    con.commit()


# driver.get('https://www.freelancer.co.uk/projects/research-writing/words-essay-ref/details')
#
# time.sleep(3)
#
# b = driver.find_elements_by_tag_name('h6')
#
# found = (len(b) == 1)
#
# print(found)
#
# driver.get('https://www.freelancer.co.uk/projects/Excel/simple-macro-made-for-excel/details')
#
# time.sleep(3)
#
# b = driver.find_elements_by_tag_name('h6')
#
# found = (len(b) == 1)
#
# print(found)
