import csv
from sys import maxint
from math import fabs
from operator import itemgetter

### I am assuming for now that the critics will be additional columns in the database.
## Let's assume we know for a fact how many attributes we have, numAttributes.  Then the
## critics will start at index numAttributes.  That is, index(firstCritic) = index(numAttributes)

def main(filePath, numAttributes, numCritics):
    data, critIndices, attrIndices, userIndices, indices = readInDB(filePath, numAttributes, numCritics)

    user = raw_input("please enter the name of the person you are trying to predict matches for")

    userMatches = getCriticMatches(user, data, indices, critics, attributes)

    userPrefs = {}
    for film in [[[listOfNewFilms]]]:
        critRatings = gatherRatingsAboutMovie(film, critIndices)
        filmAttrs = gatherFilmAttributes(film, attrIndices)
        userPrefs[film] = calculateUserRating(filmAttrs, critRatings, userMatches)
    topChoice = sorted(userPrefs.iteritems(), key=itemgetter(1), reverse=True)[0]

    print "we think that user " + user + " would really enjoy the film " + topChoice[0] + " and will give it a rating of " + str(topChoice[1])

def readInDB(filePath, numAttributes, numCritics):
    reader = csv.reader(open(filePath, 'Ur'))
    index = 0
    indices = {}
    critics = {}
    attributes = {}
    users = {}
    for field in reader.fieldnames:
        indices[field] = index
        index += 1
        if index >= numAttributes and index < numAttributes + numCritics:
            critics[field] = index - 1
        if index < numAttributes:
            attributes[field] = index - 1
        if index >= numCritics:
            users[field] = index - 1
    reader.next() # is this necessary?  I dont want to skip the first row
    data = {}
    for row in reader:
        data[row[0]] = row[1:]
    return (data, critics, attributes, users, indices)

### I am assuming for now that the critics will be additional columns in the database.
## Let's assume we know for a fact how many attributes we have, numAttributes.  Then the
## critics will start at index numAttributes.  That is, index(firstCritic) = index(numAttributes)
## colLabels will be column indexes

def WhatGroupLikes(data, group, attributes):
    ratings = {}
    for person in group.keys():
        ratings[person] = {}
        ratings[person]["QRatings"] = getAttributeScores(data, attributes, group[person])
    return ratings

def getAttributeScores(data, attributeFields, raterCol):
    ## This can be used for users as well; we need to figure out how to split users from critics.
    numAttr = 0
    raterSum = 0
    ratings = {}
    for attribute in attributeFields.keys():
        for film in data.keys():
            if data[film][raterCol] == 0: continue
            if data[film][attributeFields[attribute]] == 1:
                raterSum += data[film][raterCol]
                numAttr += 1
        try:
            ratings[attribute] = raterSum / numAttr
        except: ratings[attribute] = None
    return ratings

def getCriticMatches(user, data, indices, critics, attributes):
    criticRatings = WhatGroupLikes(data, critics, attributes)
    userRatings = getAttributeScores(data, attributes, indices[user])
    userMatches[user] = {}
    for attribute in attributes.keys():
        bestMatch = sys.maxint
        for critic in critics.keys():
            if userRatings[attribute] == None or critic[attribute] == None: continue
            thisMatch = math.fabs(userRatings[attribute]-critic[attribute])
            if thisMatch < bestMatch:
                bestMatch = thisMatch
                userMatches[user][attribute] = critic #on this attribute, this user agrees most with this critic
        if attribute not in userMatches[user].keys(): userMatches[user][attribute] = None
    return userMatches

def gatherRatingsAboutMovie(movie, critics):
    ratings = {}
    for critic in critics.keys():
        ratings[critic] = movie[critics[critic]]
    return ratings

def gatherFilmAttributes(movieRow, attributes):
    movieAttr = {}
    for attribute in attributes.keys():
        movieAttr[attribute] = movieRow[attributes[attribute]]
    return movieAttr

def calculateUserRating(filmAttributes, criticRatings, userMatches):
    # userMatches here is going to be userMatches[user], i.e., a PARTICULAR user's critic matches
    # criticRatings will be a dictionary of critics, each with their rating for THIS PARTICULAR movie.  should be easy to change
    # for right now lets assume THESE film attributes come in as a dictionary; also should be easy to change to whatever works best
    totalRating = 0
    numAttributes = 0
    for attribute in filmAttributes.keys():
        if filmAttributes[attribute] == 1:
            totalRating += criticRatings[userMatches[attribute]] #this dictionary has each critic's rating stored under their name, i.e., "Peter Travers": 91
            numAttributes += 1
    finalRating = totalRating / numAttributes
    return finalRating
