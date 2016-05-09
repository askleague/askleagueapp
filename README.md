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

# Challenges
The biggest challenge we faced was getting easy to remember terms so people don't have to constantly come look at the wiki for information. We tried keeping them as simple as possible and self explanitory as possible. Even so, some of them may not be as easy as others, especially when it comes to summoner data. We asked a couple of people to go through our list and see if they made sense and we believe we found a good balance.

We faced many challenges during the process of creating the script. The majority of them came from twitter and how their system works. Primarily, the 140 character limit. Not only did we have to find a way to work with the limit, but we also had to find simple ways to display data, specifically descriptions.

We also had problems getting the script to run on a web service without interruption. These challenges were mostly due to our inexperience, but ultimately we managed to get everything settled with Amazon Web Services. Setting up a cron job that handles the services on Amazon's VPCs was the key to getting it up and running. This of course did not come with its share of headaches.

# Post-mortem
We jumped into the challenge a couple days behind, those few days could've made a huge difference in terms of testing and improvements. We were hesitant to use Python as neither of us had worked with it in the past but have heard great things about its simplicity and support. The amount of documentation and support Python has is outstanding. We had little to no trouble learning the quirks of Python and slowly fell in love with the language. We'll definitely be using it a lot more in the future, I'm glad we decided to participate in this challenge as we would not have tried to work with Python without some motivation.

We wish we could have spent more time researching different web hosts and finding one that ultimately works best rather than simply duct taping everything we have now. Amazon Web Services is a fine service but the amount of documentation for it is scarce or hard to follow. After tinkering around with it for a day we finally got everything up and running but it still isn't perfect and there is much we can improve upon.

# Future Plans
We still plan to support this application after this challenge is over. Our biggest feature we plan on releasing is duo matchmaking. Being able to quickly match yourself with other players who are looking for a quick partner for a couple of games would be awesome. This of course would require us to make this application much more secure as we would then be storing and handling summoner names and data.

We would also like to improve the requests, open them up to other regions other than NA and have better responses that aren't canned to group terms together. There are plenty of quality of life improvements that could be made to improve this application overall.
