import requests
from bs4 import BeautifulSoup

LINK_PREFIX = "https://www.freelancer.co.uk"

# Will retrieve all the data from the given weeks
def getAllTheRelevantLinks(url):
    projectLinks = []

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Gets the list of projects
    items = soup.find("ul", {"class" : "prjt"})

    # Gets all the links
    listLinks = items.contents[1].find_all("a")

    for item in listLinks:
        title = item.get("title")

        # Only look at projects that do not have a title beginning with "Project for"
        if (len(title.split("Project for")) == 1):
            projectLink = LINK_PREFIX + item.get("href")
            projectLinks.append(projectLink)


        # Calls checkProject on each individual project link
        # for item in listLinks:
        #     linkToProject = item.get("href")
        #     checkProject(PREFIX_LINK + linkToProject)
    return projectLinks
