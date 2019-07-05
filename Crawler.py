import requests
from bs4 import BeautifulSoup

PREFIX_LINK = "https://www.freelancer.co.uk"

# Will retrieve all the data from the given weeks
def getAllTheRelevantLinks(links):
    links = [links[0]]
    projectLinks = []

    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Gets the list of projects
        items = soup.find("ul", {"class" : "prjt"})

        # Gets all the links
        listLinks = items.contents[1].find_all("a")

        for item in listLinks:
            title = item.get("title")

            # Only look at projects that do not have a title beginning with "Project for"
            if (len(title.split("Project for")) == 1):
                projectLink = PREFIX_LINK + item.get("href")
                projectLinks.append(projectLink)


        # Calls checkProject on each individual project link
        # for item in listLinks:
        #     linkToProject = item.get("href")
        #     checkProject(PREFIX_LINK + linkToProject)
    return projectLinks

def checkProject(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    print("Hello")

# Will crawl through the whole archive
def crawlWholeArchive():
    print("Hello")

def getThisYearApartFromLastMonth(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    yearsData = soup.find_all("ul")[1].contents[1:]

    links = yearsData[-2].find_all("a")[:-4]

    data = []

    # Get the links to the weeks and years
    for item in links:
        data.append(PREFIX_LINK + item.get("href"))

    return getAllTheRelevantLinks(data)

# Will crawl through the archived projects within the given time-frame for a given URL
def crawlArchiveByGivenURL(url, numberofYearsToView):
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

    # Builds a list of all the links of the weeks
    for i in range(len(data)):
        newData = BeautifulSoup(str(data[i]), 'html.parser')
        links = newData.find_all("a")
        for link in links:
            linksToFollow.append(PREFIX_LINK + link.get("href"))

    getAllTheRelevantLinks(linksToFollow)