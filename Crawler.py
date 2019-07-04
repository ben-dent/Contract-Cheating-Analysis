import requests
from bs4 import BeautifulSoup
from datetime import date

# Will crawl through the whole archive
def crawlWholeArchive(self):
    print("Hello")

# Will crawl through the archived projects within the given time-frame for a given URL
def crawlArchiveByGivenURL(self, url, numberofYearsToView):
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

    print("Hello")