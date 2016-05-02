import json
import string
import sys
import os, datetime
import requests
import tweepy
import textwrap
import itertools
from random import randint
from json import dumps

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
        responseTweet = processRequest(words, user)
        sendTweet(responseTweet, tweetID)

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
            values = (str(callDict['id']), str(callDict['name']))
            data[i] = dict(itertools.izip(keys, values))
            print data
            i += 1

    data_json = json.dumps(data)
    outFile = open('itemIndex.txt', 'w')
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
            values = (str(callDict['id']), str(callDict['name']))
            data[i] = dict(itertools.izip(keys, values))
            print data
            #data[int(i)] = str(callDict['id'])
            i += 1

    data_json = json.dumps(data)
    outFile = open('summonerSpellIndex.txt', 'w')
    json.dump(data_json, outFile)
    outFile.close()
    print "all summoner spells found!"

    print "searching for masteries...please wait..."
    i = 0
    keys = ()
    values = ()
    data = {}
    for x in range(6110, 6400):
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery/' + str(x) + + '?' + riotKey
        callString = requests.get(url)
        if (callString.status_code == 200):
            callDict = json.loads(callString.content)
            print "Mastery Found: " + str(callDict['id'])
            keys = ('id', 'name')
            values = (str(callDict['id']), str(callDict['name']))
            data[i] = dict(itertools.izip(keys, values))
            print data
            i += 1

    data_json = json.dumps(data)
    outFile = open('masteryIndex.txt', 'w')
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
            values = (str(callDict['id']), str(callDict['name']))
            data[i] = dict(itertools.izip(keys, values))
            print data
            i += 1

    data_json = json.dumps(data)
    outFile = open('championIndex.txt', 'w')
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

def getSummoner(username, value, ranked='unranked', champ=0, season='SEASON2016', mode='unranked 5v5'):
    "This calls the API for all summoner information"

    url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + username + '?' + riotKey
    print url

    #Because we pass blank values sometimes, we have to reset these to their default values
    if (ranked == ''):
        ranked = 'unranked'

    if (season == ''):
        season = 'SEASON2016'

    if (mode == ''):
        mode = "Unranked"

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

            #Find that champion's stats
            for champion in callDict['champions']:
                print repr(champion['id'])
                print repr(champ)
                if str(champion['id']) == champ:
                    print "This user does use this champion!!"
                    print "that champion's id is: " + champ
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
        for element in reversed(tweets):
            element = "@" + user + ' (' + str(i) + '/' + str(len(tweets)) + ') ' + element
            i -= 1
            print element
            api.update_status(element, tweetID)
    else:
        msg = "@" + user + " " + msg
        print msg
        api.update_status(msg, tweetID)

def processRequest(words, user):
    "Processes a request made by the user"
    terms = []
    summonerName = ''
    requestedValue = ''
    rankedValue = ''
    champValue = ''
    seasonValue = ''
    modeValue = ''

    for word in words:
        terms.append(word.lower())
        print terms

    keywords = combineTerms(terms)

    querySize = len(keywords)
    print "query size is " + str(querySize)
    #First, check if first word is a valid keyword
    if (keywords[0] == 'summoner' or 'champion' or 'item' or 'mastery' or 'spell' or 'status'):
        #Next, check the keywords that come after after a valid keyword until the next valid keyword appear
        #If first keyword is summoner, go through the special summoner call
        if (keywords[0] == 'summoner'):
            print "Valid query requested!"

            summonerName = keywords[1]
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
                    elif (keywords[x] == 'unranked'):
                        print "Unranked request made======"
                        rankedValue = 'unranked'

                    if (keywords[x] in ('2013', '2014', '2015', '2016')):
                        print "Season request made========"
                        seasonValue = getTerm(keywords[x], seasonLib)
                    else:
                        check = getTerm(keywords[x], statLib)
                        if check != '':
                            requestedValue = check
                            print "Stat request made======="

                        check = getTerm(keywords[x], modeLib)
                        print keywords[x] + " == " + check
                        if check != '':
                            modeValue = check
                            print "Mode request made======="

                        check = getChamp(keywords[x])
                        print keywords[x] + " == " + check
                        if check != '':
                            champValue = check
                            print "Champ request made======"
                else:
                    break

            print "\nsummoner value: " + summonerName
            print "requested value: " + requestedValue
            print "ranked value: " + rankedValue
            print "champion value: " + champValue
            print "season value: " + seasonValue
            print "mode value: " + modeValue

            #Now we have all the terms, make the call with whatever terms were given
            #requestedValue = keywords[x + 1]
            print "user is asking for " + summonerName + "'s " + requestedValue + " in the mode " + modeValue
            answer = getSummoner(summonerName, requestedValue, rankedValue, champValue, seasonValue, modeValue)
            tweetMessage = requestedValue + " " + str(answer)
            print tweetMessage
            return tweetMessage
        elif (keywords[0] == 'champion'):
            print keywords[0] + " information requested"
            check = getChamp(keywords[1])
            print keywords[1] + " == " + check
            if check != '':
                champValue = check
                print "Champ request made======"
            else:
                print "champion not found!"

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            value = keywords[2]
            check = getTerm(value, champStatLib)
            if check != '':
                value = check
            else:
                print "first value not found!"

            value2 = ''
            if querySize > 3:
                value2 = keywords[3]
                check = getTerm(value2, champStatLib)
                if check != '':
                    value2 = check
                else:
                    print "second value not found!"

            r = staticAPI(keywords[0], champValue, 'champData=all')
            callDict = json.loads(r.content)

            if value == 'passive':
                if value2 != '':
                    requestedValue = callDict[value][value2]
                    print "Passive " + value2 + " is " + requestedValue
                else:
                    requestedValue = callDict[value]['name']
                    print "Passive name is " + requestedValue
            elif (len(value) == 1):
                print "val length is " + str(len(value))
                if value2 != '':
                    if value2 == 'name' or value2 == 'sanitizedDescription':
                        requestedValue = callDict['spells'][int(value)][value2]

                    if value2 == 'cost' or value2 == 'cooldown':
                        requestedValue = ''
                        for val in callDict['spells'][int(value)][value2]:
                            requestedValue = requestedValue + str(val) + "/"


                    print "Spell" + value2 + " is " + requestedValue
                else:
                    requestedValue = callDict['spells'][int(value)]['name']
                    print "Spell name is " + requestedValue

            if value == 'title':
                print value
                requestedValue = callDict[value]
                print "Title is " + requestedValue

            if value2 != '':
                tweetMessage = value + " " + value2 + " " + requestedValue
            else:
                tweetMessage = value + " " + requestedValue
            print tweetMessage
            return tweetMessage

        if keywords[0] == 'item':
            print "ITEM REQUEST!"
        elif keywords[0] == 'mastery':
            print keywords[0] + " information requested"
            check = getMastery(keywords[1])
            print keywords[1] + " == " + check
            if check != '':
                masteryValue = check
                print "mastery request made======"
            else:
                print "mastery not found!"

            #We have to get the 2 values the user is searching for in some cases
            #by default, the second value is usually just name
            value = keywords[2]
            check = getTerm(value, masteryLib)
            if check != '':
                value = check
            else:
                print "first value not found!"

            r = staticAPI(keywords[0], masteryValue, 'masteryData=all')
            callDict = json.loads(r.content)

            if value == 'sanitizedDescription':
                print value
                requestedValue = callDict[value][0]
                print "Description is " + requestedValue
            else:
                print value
                requestedValue = callDict[value]
                print value + " is " + str(requestedValue)

            tweetMessage = value + " " + str(requestedValue)
            print tweetMessage
            return tweetMessage

        if keywords[0] == 'spell':
            print "SPELL REQUEST!"
        elif keywords[0] == 'status':
            print keywords[0] + " information requested"
            check = getTerm(keywords[1], statusLib)
            if check != '':
                value = check
            else:
                print "First value not found!"

            #r = staticAPI(keywords[0])

def combineTerms(keywords):
    "Combs through every keyword and attempts to group them together"

    #Because the first two keywords will always be twitter handle & a search term
    #we can ignore keyword1 and start the new list with keyword2
    newKeywords = []
    querySize = len(keywords)
    newKeywords.append(keywords[1])
    x = 1
    if (keywords[1] == 'summoner'):
        x = 3
        summonerName = keywords[x - 1]
        while True:
            #print "checking term " + str(x) + " / " + str(querySize)
            if (keywords[x] != '?' or x > querySize):
                summonerName = summonerName + ' ' + keywords[x]
                #print "current name is: " + summonerName
                x += 1
            else:
                newKeywords.append(summonerName)
                #print "Summoner name has been found!"
                break

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
                    print "current term is " + keywords[x]
                    check = termCheck(keywords[x], lib)
                else:
                    possibleTerm = term + " " + keywords[x]
                    print "current term is " + possibleTerm
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
            newKeywords.append(term)
            #print "final keywords are"
            print newKeywords
            break

        #print "Checked all libs!"
        #print "term is " + term
        #print "possible term is " + possibleTerm
        #print "Number of passes: " + str(libPass) + " out of " + str(len(fullLib))
        if (libPass >= len(fullLib) and term != possibleTerm) or (x == querySize):
            print "A Full pass was made!"
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
        if (lib == champNameLib):
            #print " current key is: " + lib[key]['name']
            #print repr(lib[key]['name']) + " == " + repr(word)
            if word in lib[key]['name'].lower():
                print lib[key]['name'] + " == " + word
                return True
                break

        if lib == masteryNameLib:
            #print "Current key is: " + lib[key]['name']
            #print repr(lib[key]['name']) + " == " + repr(word)
            if word in lib[key]['name'].lower():
                print lib[key]['name'] + " == " + word
                return True
                break
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

def getChamp(champName):
    "Looks up champion ID for name"

    for key in champNameLib:
        #print "checking key " + str(key)
        if champNameLib[key]['name'].lower() == champName:
            print "Found: " + champNameLib[key]['name']
            return champNameLib[key]['id']

    return ''

def getMastery(masteryName):
    "Looks up Mastery ID for name"

    for key in masteryNameLib:
        #print "checking key " + str(key)
        if masteryNameLib[key]['name'].lower() == masteryName:
            print "Found: " + masteryNameLib[key]['name']
            return masteryNameLib[key]['id']

    return ''

riotKey = <RIOT API KEY HERE>
user = ''

#Check current league version
r = staticAPI('versions')
callDict = json.loads(r.content)
inFile = open('versions.txt', 'r')
inDict = json.load(inFile)
inFile.close()

#print inDict[0]
#print callDict[0]
# if (inDict[0] != callDict[0]):
#     buildLibrary()

#buildLibrary()

inFile = open('itemIndex.txt', 'r')
inString = json.load(inFile)
itemDict = json.loads(inString)
inFile.close()

itemID = getRandomEntity(itemDict)
r = staticAPI('item', str(itemID['id']))
inFile = open('summonerSpellIndex.txt', 'r')
inString = json.load(inFile)
summonerSpellDict = json.loads(inString)
inFile.close()

spellID = getRandomEntity(summonerSpellDict)
r = staticAPI('summoner-spell', str(spellID['id']))

inFile = open('masteryNameLib.txt', 'r')
inString = json.load(inFile)
masteryDict = json.loads(inString)
inFile.close()

masteryID = getRandomEntity(masteryDict)
r = staticAPI('mastery', str(masteryID['id']))

inFile = open('champNameLib.txt', 'r')
inString = json.load(inFile)
championDict = json.loads(inString)
inFile.close()

championID = getRandomEntity(championDict)
r = staticAPI('champion', str(championID['id']), 'champData=spells')

#Open and store all needed libraries
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

inFile = open('itemLib.txt', 'r')
itemLib = json.load(inFile)
inFile.close()

inFile = open('masteryNameLib.txt', 'r')
inString = json.load(inFile)
masteryNameLib = json.loads(inString)
inFile.close()

inFile = open('masteryLib.txt', 'r')
masteryLib = json.load(inFile)
inFile.close()

inFile = open('spellLib.txt', 'r')
spellLib = json.load(inFile)
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

fullLib = (statLib, champNameLib, champStatLib, itemLib, masteryNameLib, masteryLib, spellLib, statusLib, modeLib, seasonLib)

print "Connecting to twitter...please wait..."
#Sets up all the needed twitter info
CONSUMER_KEY = <CONSUMER KEY>
CONSUMER_SECRET = <CONSUMER SECRET>
ACCESS_KEY = <ACCESS KEY>
ACCESS_SECRET = <ACCESS SECRET>
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
print "successfully connected to twitter!\n"

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@leagueask'])

# callDict = json.loads(r.content)
# tweetMessage = callDict['spells'][0]['sanitizedDescription']
# print tweetMessage
# sendTweet(tweetMessage)
