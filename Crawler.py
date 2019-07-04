import requests
from bs4 import BeautifulSoup
from datetime import date


def getAllTheData():
    print("Ok")

# Will crawl through the whole archive
def crawlWholeArchive():
    print("Hello")

# Will crawl through the archived projects within the given time-frame for a given URL
def crawlArchiveByGivenURL(url, numberofYearsToView):
    # Get the (zero-indexed) week number
    thisYear = date.today().isocalendar()[0]

    # Get the data from the page
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    yearsData = soup.find_all("ul")[1].contents[1:]
    data = []

    # Get the links to the weeks and years
    for i in range(len(yearsData)):
        if (yearsData[i] != "\n"):
            data.append(yearsData[i])

    # Calculates the index to use in the fetched data
    index = numberofYearsToView * -1

    # Gets all the links to weeks and for the desired range of years
    data = data[index:]

    linksToFollow = []

    for i in range(len(data)):
        newData = BeautifulSoup(str(data[i]), 'html.parser')
        links = newData.find_all("a")
        for link in links:
            linksToFollow.append("https://www.freelancer.co.uk" + link.get("href"))

    getAllTheData()