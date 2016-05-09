#!/usr/bin/env python
import json
import string
import sys
import os, datetime
import requests
import tweepy
import textwrap
import itertools
import logging
from logging import handlers
from random import randint
from json import dumps
from quicklock import singleton

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        msg = json.loads(data.strip())
        retweet = msg['retweeted']
        global user
        user = msg['user']['screen_name']
        print user + " says " + msg['text']

        tweetID = msg['id']
        print "tweet id is " + str(tweetID)
        words = msg['text'].split()
        try:
            responseTweet = processRequest(words, user)
        except:
            crashLogger.exception('Got exception on processing request')
            raise

        if responseTweet == 'fail':
            print "This was a bad request"
        else:
            try:
                sendTweet(responseTweet, tweetID)
            except:
                crashLogger.exception('Got exception on processing request')
                raise

def buildLibrary():
    "Builds library of all trivia things and saves them as jsons"

    print "searching for items...please wait..."
    i = 0
    keys = ()
    values = ()
    data = {}
    for x in range(1001, 3932):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/' + str(x) + '?'+ riotKey
        #print url
        callString = requests.get(url)
        #print rString.content
        if (callString.status_code == 200):
            callDict = json.loads(callString.content)
            print "Item found: " + str(callDict['id'])
            keys = ('id', 'name')
            try:
                values = (str(callDict['id']), str(callDict['name']))
                data[i] = dict(itertools.izip(keys, values))
                print data
            except:
                print "all good just ignore"
                continue

            i += 1

    data_json = json.dumps(data)
    outFile = open('itemNameLib.txt', 'w')
    json.dump(data_json, outFile)
    outFile.close()
    print "all items found!"

    print "searching for spells...please wait..."
    i = 0
    keys = ()
    values = ()
    data = {}
    for x in range(0, 40):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell/' + str(x) + '?&' + riotKey
        callString = requests.get(url)
        if (callString.status_code == 200):
            callDict = json.loads(callString.content)
            print "Summoner Spell Found: " + str(callDict['id'])
            keys = ('id', 'name')
            try:
                values = (str(callDict['id']), str(callDict['name']))
                data[i] = dict(itertools.izip(keys, values))
                print data
            except:
                print "all good just ignore"
                continue

            #data[int(i)] = str(callDict['id'])
            i += 1

    data_json = json.dumps(data)
    outFile = open('spellNameLib.txt', 'w')
    json.dump(data_json, outFile)
    outFile.close()
    print "all summoner spells found!"

    print "searching for masteries...please wait..."
    i = 0
    keys = ()
    values = ()
    data = {}
    for x in range(6110, 6400):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery/' + str(x) + '?' + riotKey
        callString = requests.get(url)
        if (callString.status_code == 200):
            callDict = json.loads(callString.content)
            print "Mastery Found: " + str(callDict['id'])
            keys = ('id', 'name')
            try:
                values = (str(callDict['id']), str(callDict['name']))
                data[i] = dict(itertools.izip(keys, values))
            except:
                print "all good just ignore"
                continue

            print data
            i += 1

    data_json = json.dumps(data)
    outFile = open('masteryNameLib.txt', 'w')
    json.dump(data_json, outFile)
    outFile.close()
    print "all summoner spells found!"

    print "searching for champions...please wait..."
    i = 0
    keys = ()
    values = ()
    data = {}
    for x in range(0, 500):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(x) + '?' + riotKey
        callString = requests.get(url)
        if (callString.status_code == 200):
            callDict = json.loads(callString.content)
            print "Champion Found: " + str(callDict['id'])
            keys = ('id', 'name')
            try:
                values = (str(callDict['id']), str(callDict['name']))
                data[i] = dict(itertools.izip(keys, values))
            except:
                print "all good just ignore"
                continue

            print data
            i += 1

    data_json = json.dumps(data)
    outFile = open('champNameLib.txt', 'w')
    json.dump(data_json, outFile)
    outFile.close()
    print "all champions found!"

def staticAPI(endpoint, entityID='', query=''):
    "This calls the api"

    if (entityID == ''):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/' + endpoint + '?' + riotKey
    elif (query == ''):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/' + endpoint + '/' + str(entityID) + '?' + riotKey
    else:
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/' + endpoint + '/' + str(entityID) + '?' + str(query) + '&' + riotKey
    #print url
    getRequest = requests.get(url)
    return getRequest

def statusAPI():
    "This calls the status API"

    url = 'http://status.leagueoflegends.com/shards/na'

    getRequest = requests.get(url)
    return getRequest

def getSummoner(username, value, ranked='unranked', champ=0, season='SEASON2016', mode='unranked 5v5'):
    "This calls the API for all summoner information"

    url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + username + '?' + riotKey
    print url

    #Because we pass blank values sometimes, we have to reset these to their default values
    if (ranked == ''):
        ranked = 'unranked'

    if (value == ''):
        if ranked == 'ranked':
            value = 'totalSessionsWon'
        else:
            value = 'wins'

    if (season == ''):
        season = 'SEASON2016'

    if (mode == ''):
        mode = "Unranked"

    if (champ == ''):
        champ = '0'

    summonerID = ''
    requestedValue = ''
    callString = requests.get(url)
    if (callString.status_code == 200):
        callDict = json.loads(callString.content)
        summonerID = callDict[username.replace(" ", "")]['id']
        print "summoner ID: " + str(summonerID)
    else:
        #A twitter response should be made here to tweet that the user does not exist
        print "Code was: " + str(callString.status_code)

    if (summonerID != ''):
        if (ranked == 'ranked'):
            print "checking ranked stats"
            url = 'https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(summonerID) + '/ranked?season=' + season + '&' + riotKey
            print url
            callString = requests.get(url)
            callDict = json.loads(callString.content)

            if value == 'wins':
                value = 'totalSessionsWon'

            #Find that champion's stats
            for champion in callDict['champions']:
                #print repr(champion['id']) + " == " + repr(champ)
                if str(champion['id']) == champ:
                    print "This user does use this champion!!"
                    print "that champion's id is: " + champ + " for " + str(value)
                    requestedValue = champion['stats'][value]
                    break

            print "Requested value was " + str(requestedValue)
            return requestedValue
        elif (ranked == 'unranked'):
            url = 'https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(summonerID) + '/summary?season=' + season + '&' + riotKey
            print url
            callString = requests.get(url)
            callDict = json.loads(callString.content)

            #Once we know what the user is looking for, make the call to retrive the term they want
            print "mode value is: " + mode
            print "search value is: " + value
            for modes in callDict['playerStatSummaries']:
                if (modes['playerStatSummaryType'] == mode):
                    print "This is the correct mode:\n"
                    print "Requested mode: " + str(mode)
                    if (value == 'wins'):
                        requestedValue = modes[value]
                    else:
                        requestedValue = modes['aggregatedStats'][value]
                    print requestedValue
                    return requestedValue
                    break

def getRandomEntity(jsonDict):
    "Makes a call to API for the desired entity"
    rID = 0
    dictLength = len(jsonDict) - 1
    ran = randint(0,dictLength)
    rID = jsonDict[str(ran)]
    return rID

def sendTweet(msg, tweetID=''):
    "This formats and sends tweets"

    maxChars = 132 - len(user)
    tweets = textwrap.wrap(msg, width = maxChars)
    numMessages = len(tweets)
    if (numMessages > 1):
        i = numMessages
        try:
            for element in reversed(tweets):
                element = "@" + user + ' (' + str(i) + '/' + str(len(tweets)) + ') ' + element
                i -= 1
                print element
                api.update_status(element, tweetID)
        except:
            print "Error sending tweetID"
            crashLogger.exception('Got exception on processing request')
            pass

    else:
        msg = "@" + user + " " + msg
        print msg
        try:
            api.update_status(msg, tweetID)
        except:
            print "Error sending tweetID"
            crashLogger.exception('Got exception on processing request')
            pass

def processRequest(words, user):
    "Processes a request made by the user"
    terms = []
    summonerName = ''
    requestedValue = ''
    rankedValue = ''
    champValue = ''
    seasonValue = ''
    modeValue = ''
    outRanked = ''
    outChamp = ''
    outSeason = ''
    outStat = ''
    outMode = ''
    outChamp = ''

    for word in words:
        terms.append(word.lower())
        print terms

    keywords = combineTerms(terms)
    print keywords

    querySize = len(keywords)
    #print "query size is " + str(querySize)
    #First, check if first word is a valid keyword
    if keywords[0] in possibleKeys:
        #Next, check the keywords that come after after a valid keyword until the next valid keyword appear
        #If first keyword is summoner, go through the special summoner call
        if (keywords[0] == 'summoner'):
            print "Valid query requested!"

            print len(keywords)
            if len(keywords) > 1:
                summonerName = keywords[1]
            else:
                return 'fail'
            #If the user specified any optional variables, keep going to find them!
            #First, we need to know if the user is requesting a ranked or unranked term
            #if left blank, we just assume its unranked
            x = 1
            while True:
                x += 1
                print "checking term " + str(x) + " / " + str(querySize)
                if (x < querySize):
                    print "current term is " + keywords[x]
                    if (keywords[x] == 'ranked'):
                        print "Ranked request made======="
                        rankedValue = 'ranked'
                        outRanked = keywords[x]
                    elif (keywords[x] == 'unranked'):
                        print "Unranked request made======"
                        rankedValue = 'unranked'
                        outRanked = keywords[x]

                    if (keywords[x] in ('2013', '2014', '2015', '2016')):
                        print "Season request made========"
                        seasonValue = getTerm(keywords[x], seasonLib)
                        outSeason = keywords[x]
                    else:
                        check = getTerm(keywords[x], statLib)
                        if check != '':
                            requestedValue = check
                            outStat = keywords[x]
                            print requestedValue
                            print "Stat request made======="

                        check = getTerm(keywords[x], modeLib)
                        #print keywords[x] + " == " + check
                        if check != '':
                            modeValue = check
                            outMode = keywords[x]
                            print "Mode request made======="
                        else:
                            modeValue = 'Unranked'
                            outMode = 'unranked 5v5'

                        check = getChampID(keywords[x])
                        print keywords[x] + " == " + check
                        if check != '':
                            champValue = check
                            outChamp = keywords[x]
                            print "Champ request made======"
                else:
                    break

            print "\nsummoner value: " + summonerName
            print "requested value: " + requestedValue
            print "ranked value: " + rankedValue
            print "champion value: " + champValue
            print "season value: " + seasonValue
            print "mode value: " + modeValue
            print "out ranked: " + outRanked
            print "out champ: " + outChamp
            print "outSeason: " + outSeason
            print "outStat: " + outStat
            print "outMode: "+ outMode
            print "outChamp: " + outChamp

            #Now we have all the terms, make the call with whatever terms were given
            #requestedValue = keywords[x + 1]
            print "user is asking for " + summonerName + "'s " + requestedValue + " in the mode " + modeValue
            try:
                answer = getSummoner(summonerName, requestedValue, rankedValue, champValue, seasonValue, modeValue)
            except:
                crashLogger.exception('That stat does not exist')
                return 'fail'

            if answer == None:
                return 'fail'

            if rankedValue == 'ranked':
                tweetMessage = summonerName + "'s " + outStat + " for " + outChamp + " is " + str(answer)
            else:
                tweetMessage = summonerName + "'s " + outStat + " in mode " + outMode + " is " + str(answer)

            print tweetMessage
            return tweetMessage
        elif (keywords[0] == 'champion'):
            print keywords[0] + " information requested"

            print str(len(keywords))
            if len(keywords) > 2:
                check = getChampID(keywords[1])
                print keywords[1] + " == " + check
                if check != '':
                    champValue = check
                    print "Champ request made======"
                else:
                    print "champion not found!"
                    return 'fail'
            else:
                return 'fail'

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            value = keywords[2]
            check = getTerm(value, champStatLib)
            if check != '':
                value = check
                outSkill = keywords[2]
            else:
                value = ''
                print "first value not found!"
                return 'fail'

            value2 = ''
            if querySize > 3:
                value2 = keywords[3]
                check = getTerm(value2, champStatLib)
                if check != '':
                    value2 = check
                else:
                    value2 = 'name'
                    print "second value not found!"
            else:
                value2 = 'name'

            r = staticAPI(keywords[0], champValue, 'champData=all')
            callDict = json.loads(r.content)

            if value == 'passive':
                if value2 == 'sanitizedDescription':
                    requestedValue = callDict[value][value2]
                    tweetMessage = callDict[value]['name'] + ": " + requestedValue
                elif value2 == 'name':
                    requestedValue = callDict[value]['name']
                    tweetMessage = keywords[1] + "'s passive is " + requestedValue
            elif (len(value) == 1):
                print "val length is " + str(len(value))
                if value2 != '':
                    if value2 == 'name' or value2 == 'sanitizedDescription':
                        requestedValue = callDict['spells'][int(value)][value2]
                        if value2 == 'name':
                            tweetMessage = keywords[1] + "'s " + outSkill.upper() + " is " + requestedValue
                        else:
                            tweetMessage = keywords[1] + ": " + requestedValue

                    if value2 == 'cost':
                        requestedValue = ''
                        for val in callDict['spells'][int(value)][value2]:
                            requestedValue = requestedValue + str(int(val)) + "/"

                        tweetMessage = callDict['spells'][int(value)]['name'] + "'s cost: " + requestedValue
                    elif value2 == 'cooldown':
                        for val in callDict['spells'][int(value)][value2]:
                            requestedValue = requestedValue + str(int(val)) + "/"

                        tweetMessage = callDict['spells'][int(value)]['name'] + "'s cooldown: " + requestedValue
                else:
                    requestedValue = callDict['spells'][int(value)]['name']
                    tweetMessage = keywords[1] + "'s " + outSkill.upper() + " is " + requestedValue

            if value == 'title':
                requestedValue = callDict[value]
                tweetMessage = keywords[1] + "'s title is " + requestedValue

            try:
                print tweetMessage
                return tweetMessage
            except:
                return 'fail'

        if keywords[0] == 'item':
            print keywords[0] + " information requested"
            if len(keywords) > 1:
                check = getItemID(keywords[1])
                print keywords[1] + " == " + check
                if check != '':
                    itemValue = check
                    print "item request made======"
                else:
                    print "item not found!"
                    return 'fail'
            else:
                return 'fail'

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            print len(keywords)
            if len(keywords) > 2:
                value = keywords[2]
                check = getTerm(value, itemStatLib)
                if check != '':
                    value = check
                    outValue = keywords[2]
                else:
                    print "first value not found!"
                    return 'fail'
            else:
                value = 'sanitizedDescription'

            r = staticAPI(keywords[0], itemValue, 'itemData=all')
            callDict = json.loads(r.content)

            if value == 'sanitizedDescription':
                print value
                requestedValue = callDict[value]
                print "Description is " + requestedValue
                tweetMessage = keywords[1] + ": " + str(requestedValue)
            elif value == 'into':
                print value
                buildList = []
                for item in callDict['into']:
                    itemName = getItemName(item)
                    print "Item found: " + itemName
                    buildList.append(itemName)
                    print buildList

                nameString = buildList[0]
                for name in buildList[1:]:
                    nameString = nameString + ", " + name
                tweetMessage = keywords[1] + " builds into " + nameString
            else:
                print value
                requestedValue = callDict['gold'][value]
                print value + " is " + str(requestedValue)
                if outValue == 'sell':
                    tweetMessage = keywords[1] + " sells for " + str(requestedValue)
                else:
                    tweetMessage = keywords[1] + "'s " + outValue + " is " + str(requestedValue)

            print tweetMessage
            return tweetMessage
        elif keywords[0] == 'mastery':
            print keywords[0] + " information requested"
            if len(keywords) > 1:
                check = getMastery(keywords[1])
                print keywords[1] + " == " + check
                if check != '':
                    masteryValue = check
                    print "mastery request made======"
                else:
                    print "mastery not found!"
                    return 'fail'
            else:
                return 'fail'

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            if len(keywords) > 2:
                value = keywords[2]
                check = getTerm(value, masteryLib)
                if check != '':
                    value = check
                else:
                    print "first value not found!"
                    return 'fail'
            else:
                value = 'sanitizedDescription'

            r = staticAPI(keywords[0], masteryValue, 'masteryData=all')
            callDict = json.loads(r.content)

            if value in masterykeys:
                if value == 'sanitizedDescription':
                    print value
                    requestedValue = callDict[value][0]
                    print "Description is " + requestedValue
                    tweetMessage = keywords[1] + ": " + str(requestedValue)
                else:
                    print value
                    requestedValue = callDict[value]
                    print value + " is " + str(requestedValue)
                    if keywords[2] == 'ranks':
                        tweetMessage = keywords[1] + " has " + str(requestedValue) + " rank(s)"
                    else:
                        tweetMessage = keywords[1] + " belongs to the " + str(requestedValue) + " tree"
            else:
                return 'fail'

            print tweetMessage
            return tweetMessage

        if keywords[0] == 'spell':
            print keywords[0] + " information requested"
            if len(keywords) > 1:
                check = getSpellID(keywords[1])
                print keywords[1] + " == " + check
                if check != '':
                    spellValue = check
                    print "Spell request made======"
                else:
                    print "Spell not found!"
                    return 'fail'
            else:
                return 'fail'

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            if len(keywords) > 2:
                value = keywords[2]
                check = getTerm(value, spellStatLib)
                if check != '':
                    value = check
                else:
                    print "first value not found, using default value!"
                    return 'fail'
            else:
                value = 'sanitizedDescription'

            r = staticAPI('summoner-spell', spellValue, 'spellData=all')
            callDict = json.loads(r.content)

            if keywords[2] == 'cooldown':
                requestedValue = callDict[value][0]
                tweetMessage = keywords[1] + " has a " + str(int(requestedValue)) + " second cooldown"
            elif keywords[2] == 'level':
                requestedValue = callDict[value]
                tweetMessage = keywords[1] + " requires summoner level " + str(requestedValue)
            elif keywords[2] == 'desc':
                requestedValue = callDict[value]
                tweetMessage = keywords[1] + ": " + requestedValue

            print tweetMessage
            return tweetMessage
        elif keywords[0] == 'status':
            print keywords[0] + " information requested"
            if len(keywords) > 1:
                check = getTerm(keywords[1], statusLib)
                if check != '':
                    value = check
                    print "Status request made======="
                else:
                    print "First value not found!"
                    return 'fail'
            else:
                return 'fail'

            r = statusAPI()
            callDict = json.loads(r.content)

            incidents = ''
            incidentContent = ''
            serviceStatus = ''
            serviceName = ''
            print "value is " + str(value)
            serviceStatus = callDict['services'][int(value)]['status']
            serviceName = callDict['services'][int(value)]['name']
            incidents = callDict['services'][int(value)]['incidents']
            print serviceStatus
            print serviceName
            print len(incidents)
            if len(incidents) > 0:
                print "this made it in here"
                incidentContent = callDict['services'][int(value)]['incidents'][0]['updates'][0]['content']
                print incidentContent
                tweetMessage = serviceName + " is " + serviceStatus + '.\n' + incidentContent
            else:
                tweetMessage = serviceName + " is " + serviceStatus

            print tweetMessage
            return tweetMessage

        if keywords[0] == 'rotation':
            print keywords[0] + " information requested"
            value = keywords[0]
            rotationList = []
            #rotationNames = []
            url = 'https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&' + riotKey
            r = requests.get(url)
            callDict = json.loads(r.content)
            for champ in callDict['champions']:
                champName = getChampName(champ['id'])
                print "Champion found: " + champName
                rotationList.append(champName)
                print rotationList

            nameString = rotationList[0]
            for name in rotationList[1:]:
                nameString = nameString + ", " + name

            tweetMessage = "Rotation: " + nameString
            print tweetMessage
            return tweetMessage
    else:
        return 'fail'

def combineTerms(keywords):
    "Combs through every keyword and attempts to group them together"

    #Because the first two keywords will always be twitter handle & a search term
    #we can ignore keyword1 and start the new list with keyword2
    newKeywords = []
    querySize = len(keywords)
    print "this is this long: " + str(querySize)
    newKeywords.append(keywords[1])
    x = 1
    if keywords[1] == 'summoner':
        if querySize > 2:
            x = 3
            summonerName = keywords[x - 1]
            while True:
                print "checking term " + str(x) + " / " + str(querySize)
                if x < querySize and keywords[x] != '?':
                    print "I GOT IN! " + str(x)
                    summonerName = summonerName + ' ' + keywords[x]
                    print "current name is: " + summonerName
                    x += 1
                else:
                    newKeywords.append(summonerName)
                    print "Summoner name has been found!"
                    break
        else:
            return newKeywords

    #Now we have the name, combine the rest of the terms if possible
    check = ''
    term = ''
    possibleTerm = ''
    while True:
        x += 1
        if (x < querySize):
            libPass = 0
            for lib in fullLib:
                #print "checking term " + str(x) + " / " + str(querySize)
                if term == '':
                    #print "current term is " + keywords[x]
                    check = termCheck(keywords[x], lib)
                else:
                    possibleTerm = term + " " + keywords[x]
                    #print "current term is " + possibleTerm
                    check = termCheck(possibleTerm, lib)

                if check:
                    if term == '':
                        term = keywords[x]
                        #print "Since term was blank, it is now " + term
                    else:
                        term = possibleTerm
                        #print "Term was not blank, it is now " + term
                    break
                libPass += 1
        else:
            #print "Every single word has been checked!"
            if term != '':
                newKeywords.append(term)

            #print "final keywords are"
            print newKeywords
            break

        #print "Checked all libs!"
        #print "term is " + term
        #print "possible term is " + possibleTerm
        #print "Number of passes: " + str(libPass) + " out of " + str(len(fullLib))
        if (libPass >= len(fullLib) and term != possibleTerm) or (x == querySize):
            #print "A Full pass was made!"
            newKeywords.append(term)
            term = ''
            possibleTerm = ''
            x -= 1

        #newKeywords.append(term)
        #print "current keywords are "
        print newKeywords


    print newKeywords
    return newKeywords

def termCheck(word, lib):
    "Check to see if term is in a library"

    for key in lib:
        if lib in nameLibs:
            #print " current key is: " + lib[key]['name']
            #print repr(lib[key]['name']) + " == " + repr(word)
            if word in lib[key]['name'].lower():
                print lib[key]['name'] + " == " + word
                return True
                break

        # if lib == masteryNameLib:
        #     #print "Current key is: " + lib[key]['name']
        #     #print repr(lib[key]['name']) + " == " + repr(word)
        #     if word in lib[key]['name'].lower():
        #         print lib[key]['name'] + " == " + word
        #         return True
        #         break
        else:
            if word in key:
                print key + " == " + word
                return True
                break

    return False

def getTerm(term, lib):
    "Looks up a term in the specified library"
    if lib == champNameLib:
        for key in lib:
            if term == lib[key]['name'].lower():
                return lib[key]['id']
                break
    else:
        for keys in lib:
            if (keys == term):
                return lib[str(keys)]
                break

    return ''

def getChampID(champName):
    "Looks up champion ID for name"

    for key in champNameLib:
        #print "checking key " + str(key)
        if champNameLib[key]['name'].lower() == champName:
            #print "Found: " + champNameLib[key]['name']
            return champNameLib[key]['id']

    return ''

def getChampName(champID):
    "Looks up champion name for ID"

    for key in champNameLib:
        #print "Checking key " + repr(champNameLib[key]['id']) + " for id " + repr(champID)
        if champNameLib[key]['id'] == str(champID):
            #print "Found: " + champNameLib[key]['name']
            return champNameLib[key]['name']

    return ''

def getMastery(masteryName):
    "Looks up Mastery ID for name"

    for key in masteryNameLib:
        #print "checking key " + str(key)
        if masteryNameLib[key]['name'].lower() == masteryName:
            print "Found: " + masteryNameLib[key]['name']
            return masteryNameLib[key]['id']

    return ''

def getItemID(itemName):
    "Looks up item ID for name"

    for key in itemNameLib:
        if itemNameLib[key]['name'].lower() == itemName:
            return itemNameLib[key]['id']

    return ''

def getItemName(itemID):
    "Looks up item name for ID"

    for key in itemNameLib:
        if itemNameLib[key]['id'] == str(itemID):
            return itemNameLib[key]['name']

    return ''

def getSpellID(spellName):
    "Looks up spell ID for name"

    for key in spellNameLib:
        if spellNameLib[key]['name'].lower() == spellName:
            return spellNameLib[key]['id']

    return ''

def getSpellname(spellID):
    "Looks up spell name for ID"

    for key in spellNameLib:
        if spellNameLib[key]['id'] == str(spellID):
            return spellNameLib[key]['name']

    return ''

# This is used to lock multiple cron jobs from firing
singleton('resource')
LOG_FILENAME = './crashlog.txt'
crashLogger = logging.getLogger('crashLogger')
crashLogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=90000, backupCount=10)
crashLogger.addHandler(handler)
#logging.basicConfig(filename=LOG_FILENAME, mode='w', level=logging.DEBUG)

#Twitter and API Keys
CONSUMER_KEY = <CONSUMER KEY>
CONSUMER_SECRET = <CONSUMER SECRET>
ACCESS_KEY = <ACCESS KEY>
ACCESS_SECRET = <ACCESS SECRET>
riotKey = <RIOT API KEY HERE>
user = ''

#Check current league version
r = staticAPI('versions')
callDict = json.loads(r.content)
inFile = open('versions.txt', 'r')
inDict = json.load(inFile)
inFile.close()

print inDict[0]
print callDict[0]
if (inDict[0] != callDict[0]):
    try:
        buildLibrary()
        outFile = open('versions.txt', 'w')
        json_out = json.dumps(callDict)
        json.dump(callDict, outFile)
        outFile.close()
    except:
        crashLogger.exception('Got exception on building library')
        raise

#buildLibrary()

#Open and store all needed libraries
inFile = open('spellNameLib.txt', 'r')
inString = json.load(inFile)
spellNameLib = json.loads(inString)
inFile.close()

inFile = open('spellStatLib.txt', 'r')
spellStatLib = json.load(inFile)
inFile.close()

inFile = open('statLib.txt', 'r')
statLib = json.load(inFile)
inFile.close()

inFile = open('champNameLib.txt', 'r')
inString = json.load(inFile)
champNameLib = json.loads(inString)
inFile.close()

inFile = open('champStatLib.txt', 'r')
champStatLib = json.load(inFile)
inFile.close()

inFile = open('itemNameLib.txt', 'r')
inString = json.load(inFile)
itemNameLib = json.loads(inString)
inFile.close()

inFile = open('itemStatLib.txt', 'r')
itemStatLib = json.load(inFile)
inFile.close()

inFile = open('masteryNameLib.txt', 'r')
inString = json.load(inFile)
masteryNameLib = json.loads(inString)
inFile.close()

inFile = open('masteryLib.txt', 'r')
masteryLib = json.load(inFile)
inFile.close()

inFile = open('statusLib.txt', 'r')
statusLib = json.load(inFile)
inFile.close()

inFile = open('modeLib.txt', 'r')
modeLib = json.load(inFile)
inFile.close()

inFile = open('seasonLib.txt', 'r')
seasonLib = json.load(inFile)
inFile.close()

nameLibs = (champNameLib, masteryNameLib, itemNameLib, spellNameLib)
fullLib = (spellNameLib, spellStatLib, statLib, champNameLib, champStatLib, itemNameLib, itemStatLib, masteryNameLib, masteryLib, statusLib, modeLib, seasonLib)
possibleKeys = ('summoner', 'champion', 'item', 'mastery', 'spell', 'status', 'rotation')
ChampKeys = ('title', 'passive', '0', '1', '2', '3')
masterykeys = ('ranks', 'sanitizedDescription', 'masteryTree')
itemKeys = ('total', 'sanitizedDescription', 'base', 'sell', 'into')

print "Connecting to twitter...please wait..."
try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    print "successfully connected to twitter!\n"
except:
    crashLogger.exception('Got an exception setting up twitter API')
    raise

try:
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['TwitterAccountHere'])
except:
    crashLogger.exception('Got an error setting up twitter stream')
    raise

#myStream.disconnect()
# callDict = json.loads(r.content)
# tweetMessage = callDict['spells'][0]['sanitizedDescription']
# print tweetMessage
# sendTweet(tweetMessage)
