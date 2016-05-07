## Ask League
Entry for the Spring 2016 Riot Games API Challenge, using twitter to get answers in under 140 characters.

Personally, we spend a lot of time on twitter. A lot. We decided to create a system that would allow us to gain access to the API without ever having to leave our home. With Ask League, you can quickly grab information for your favorite champions or items. You can get information on summoner spells and masteries. Most handy of all, you can check the server status as well as the weekly free champion rotations.

# Implementation
We used the API provided by Riot Games and called it through this python script. The python script gathers simple information like IDs and names for champions and items and stores them for quick access. Other libraries which are used to translate more user friendly terms into terms that the API understands were added for easy communication to the API.

A twitter library is also used in order to connect to a twitter account and create a listener that constantly checks for tweets that are made to the desired twitter account. With the twitter listener running, we are able to listen to people's tweets and reply to them with the information they have requested.

#### Processing Requests
Processing a user's request is primarily done through the process request function. Here we first split the user' tweet word by word and run it through the combineTerms function in order to combine any values that may be longer that one word. Once all the words are combined and turned into keywords, we determine what data the user is asking for specifically and search for the value requested depending on the keyword that was provided. After the value is retrieved, we format the tweet response and send it back to the twitter listener which sends the response in the form of a reply tweet to the user.

#### Combining Terms
Combining terms and summoner names is done in the combineTerms function. Here we take each individual word from a tweet and compare it to all the libraries of valid terms that the API understands until a vaild match is found. Words that are not matched are simply ignored. Summoner names use a delimiter in the form of '?' to let the script know this is the end of the user's summoner name.

#### Translating for the API
Because the API uses specific keys that may be difficult to understand or are not user friendly, we had to create a _library_ that could translate more user friendly keys into keys that the API would understand. An example of this is the term "Aram" is translated into "AramUnranked5x5". Aram is much easier to remember than the key the API uses. There are also some long keys in the API that are not very friendly with the 140 character limitation enforced by twitter.

#### Hosting
Because the app needs to be on as much as possible in order to listen to requests, I needed to find a way to keep the app up and running without too many issues. For that we decided to go with amazon web service's VPC. We used S3 to store the project and download it to the VPC with every new update we made. If the script happens to crash for whatever reason, we setup a cronjob that checks it's status every 30 minutes, if the app is not up and running, it starts it right back up.

# How to Run
Running the app is fairly straight forward. First you must install python 2.7.1 and all the dependencies, these are the lines at the top of main.py that start with "import". Once thats all settled, simply open up a terminal/command prompt and navigate to the folder where you've downloaded the app. Once there, enter the command _python main.py_
