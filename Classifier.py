import sqlite3 as lite
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import re
from nltk.corpus import stopwords
from contextlib import closing
import csv

##f = open('ClassTest.txt', 'wt')
##f.close()

open('ClassTest.txt', 'w+').close()

# con = lite.connect('JobDetails.db')
# cur = con.cursor()

# cur.execute('''SELECT Title, Description, Category FROM ReviewJobs''')
#
# results = [list(each) for each in cur.fetchall()]
#
# cur.execute('''SELECT Title, Description, Category FROM Jobs''')
#
# for each in cur.fetchall():
#     results.append(list(each))
#
# a = open('ClassTest.txt', 'ab')
#
# newLine = "|"
#
# a.write(u''.join(c for c in 'Title\tDescription\tCategory' + newLine).encode('utf-8'))
#
# for r in results:
#     toWrite = "".encode('utf-8')
#     title = u''.join(c for c in r[0].replace("\n", " ")).encode('utf-8') + "\t".encode('utf-8')
#     description = u''.join(c for c in r[1]).encode('utf-8') + "\t".encode('utf-8')
#     toWrite += title + description
#     toWrite += str(r[2]).encode('utf-8') + newLine.encode('utf-8')
#     a.write(toWrite)
#
# a.close()

with lite.connect("JobDetails.db") as connection:
    with closing(connection.cursor()) as cursor:
        rows = list()
        for table_name in ["ReviewJobs", "Jobs"]:
            query = 'SELECT Title, Description, Tags, Category, CountryOfPoster, CountryOfWinner, Attachment FROM ' + table_name + " WHERE Category IS NOT NULL"
            cursor.execute(query)
            rows.extend([each[0].lower(), each[1].lower, each[2].lower(), each[3], each[4].lower(), each[5].lower(), each[6]] for each in cursor.fetchall())

    with open("ClassTest.txt", "a", encoding="utf8") as a:
        writer = csv.writer(a, delimiter="\t")
        writer.writerows([["Title", "Description", 'Tags', "Category", 'CountryOfPoster', 'CountryOfWinner', "Attachment"]])
        for row in rows:
            writer.writerows([row])

data = pd.read_csv('ClassTest.txt', delimiter="\t")

feature_names = ['Title', 'Description', 'Tags', 'CountryOfPoster', 'CountryOfWinner', 'Attachment']
X = data[feature_names].dropna()
y = data['Category'].dropna()

X.index = range(len(X))
y.index = range(len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

xTest = X_test
yTest = y_test

documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(0, len(X)):
    # Remove all the special characters
#    document = re.sub(r'\W', ' ', str(X[sen]))
#
#    # remove all single characters
#    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    document = str(X.loc[sen, :])

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)

    # Converting to Lowercase
    document = document.lower()

    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)

    documents.append(document)


from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words = stopwords.words('english'))

X = vectorizer.fit_transform(documents).toarray()

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Up to here

# from sklearn.ensemble import RandomForestClassifier
# classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
# classifier.fit(X_train, y_train)
# y_pred = classifier.predict(X_test)

# with open('text_classifier', 'rb') as training_model:
#     model = pickle.load(training_model)
#
# y_pred2 = model.predict(X_test)`
#
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# print(confusion_matrix(y_test, y_pred2))
# print(classification_report(y_test, y_pred2))
# print(accuracy_score(y_test, y_pred2))

# print(confusion_matrix(y_test,y_pred))
# print(classification_report(y_test,y_pred))
# print('Accuracy of Random Forest classifier on test set: {:.2f}\n'
#       .format(accuracy_score(y_test, y_pred)))

# with open('text_classifier', 'wb') as picklefile:
#    pickle.dump(classifier,picklefile)

# Logistic Regression
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(solver='lbfgs', multi_class='auto')
logreg.fit(X_train, y_train)
print('Accuracy of Logistic regression classifier on training set: {:.2f}'
 .format(logreg.score(X_train, y_train)))
print('Accuracy of Logistic regression classifier on test set: {:.2f}\n'
 .format(logreg.score(X_test, y_test)))
 #
##with open('classifier', 'wb') as picklefile:
##    pickle.dump(logreg,picklefile)

with open('classifier', 'rb') as training_model:
    model = pickle.load(training_model)

# y_pred2 = model.predict(X_test)

# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# print(confusion_matrix(y_test, y_pred2))
# print(classification_report(y_test, y_pred2))
# print(accuracy_score(y_test, y_pred2))

# # Decision Tree
# from sklearn.tree import DecisionTreeClassifier
# clf = DecisionTreeClassifier().fit(X_train, y_train)
# print('Accuracy of Decision Tree classifier on training set: {:.2f}'
#    .format(clf.score(X_train, y_train)))
# print('Accuracy of Decision Tree classifier on test set: {:.2f}\n'
#    .format(clf.score(X_test, y_test)))
#
# # K-Nearest Neighbours
# from sklearn.neighbors import KNeighborsClassifier
# knn = KNeighborsClassifier()
# knn.fit(X_train, y_train)
# print('Accuracy of K-NN classifier on training set: {:.2f}'
#    .format(knn.score(X_train, y_train)))
# print('Accuracy of K-NN classifier on test set: {:.2f}\n'
#    .format(knn.score(X_test, y_test)))
#
# # Linear Discriminant Analysis
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# lda = LinearDiscriminantAnalysis()
# lda.fit(X_train, y_train)
# print('Accuracy of LDA classifier on training set: {:.2f}'
#    .format(lda.score(X_train, y_train)))
# print('Accuracy of LDA classifier on test set: {:.2f}\n'
#    .format(lda.score(X_test, y_test)))
#
# # Gaussian Naive Bayes
# from sklearn.naive_bayes import GaussianNB
# gnb = GaussianNB()
# gnb.fit(X_train, y_train)
# print('Accuracy of GNB classifier on training set: {:.2f}'
#    .format(gnb.score(X_train, y_train)))
# print('Accuracy of GNB classifier on test set: {:.2f}\n'
#    .format(gnb.score(X_test, y_test)))
#
# # Support Vector Machine
# from sklearn.svm import SVC
# svm = SVC(gamma='auto')
# svm.fit(X_train, y_train)
# print('Accuracy of SVM classifier on training set: {:.2f}'
#    .format(svm.score(X_train, y_train)))
# print('Accuracy of SVM classifier on test set: {:.2f}\n'
#    .format(svm.score(X_test, y_test)))
#
# # NN 1  - MLP
# from sklearn.neural_network import MLPClassifier
# mlpClf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6,5), random_state=1)
#
# mlpClf.fit(X_train, y_train)
# print('Accuracy of MLP classifier on training set: {:.2f}'
#    .format(mlpClf.score(X_train, y_train)))
# print('Accuracy of MLP classifier on test set: {:.2f}\n'
#    .format(mlpClf.score(X_test, y_test)))



####scaler = MinMaxScaler()
####X_train = scaler.fit_transform(X_train)
####X_test = scaler.transform(X_test)
##
##

results = []

con = lite.connect('JobDetails.db')
cur = con.cursor()

for table in ['Jobs', 'ReviewJobs']:
    query = 'SELECT JobID, Title, Description, Tags, CountryOfPoster, CountryOfWinner, Attachment FROM ' + table
    cur.execute(query)

    results += [list(each) for each in cur.fetchall()]

jobIDs = []
Titles = []
Descriptions = []
Tags = []
Posters = []
Winners = []
Attachments = []

for result in results:
    jobIDs.append(result[0])
    Titles.append(result[1])
    Descriptions.append(result[2])
    Tags.append(result[3])
    Posters.append(result[4])
    Winners.append(result[5])
    Attachments.append(result[6])

d = {'JobID': jobIDs, 'Title': Titles, 'Description': Descriptions, 'Tags': Tags,
     'CountryOfPoster': Posters, 'CountryOfWinner': Winners, 'Attachment': Attachments}

data = pd.DataFrame(d)
X = data

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

documents = []

for sen in range(0, len(X)):
    # Remove all the special characters
#    document = re.sub(r'\W', ' ', str(X[sen]))
#
#    # remove all single characters
#    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    document = str(X.loc[sen, :])

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)

    # Converting to Lowercase
    document = document.lower()

    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)

    documents.append(document)

X = vectorizer.transform(documents).toarray()
X = tfidfconverter.fit_transform(X).toarray()

y_pred = logreg.predict(X)

for i in range(len(jobIDs)):
    jID = jobIDs[i]
    score = y_pred[i]

    for table in ['Jobs', 'ReviewJobs']:
        query = 'UPDATE ' + table + ' SET Score = ' + str(score) + ' WHERE JobID = ' + str(jID)
        cur.execute(query)

    con.commit()
