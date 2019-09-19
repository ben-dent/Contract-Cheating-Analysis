import sqlite3 as lite

con = lite.connect('JobDetails.db')
cur = con.cursor()

profiles = ['Rachaelray', 'charleslimnet', 'basithashmi', 'citijayamala', 'janelleanne']


for i in range(len(profiles)):
    toAdd = []

    query = "SELECT Tags FROM Reviews WHERE Profile = '" + profiles[i] + "'"
    cur.execute(query)

    results = [each[0] for each in cur.fetchall()]

    for j in range(len(results)):
        result = results[j]
        split = [each.lstrip().rstrip() for each in result.split(',')]
        toAdd += [each for each in split if each not in toAdd]

    tags = {}

    for tag in toAdd:
        query = "SELECT COUNT(ReviewID) FROM Reviews WHERE Tags LIKE '%" + tag + "%'"
        cur.execute(query)
        tags.update({tag: cur.fetchone()[0]})


    tagNumbers = sorted(list(tags.values()))[-5:]

    toShow = []

    for tag in list(tags.keys()):
        if tags.get(tag) in tagNumbers:
            toShow.append(tag)

    print(profiles[i] + ": " + str(toShow))

