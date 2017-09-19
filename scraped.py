import requests, json
from bs4 import BeautifulSoup
from flask import Flask
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, '/')

### Get Bugcrowd Programs
def BugcrowdPrograms():
    bugcrowdURL = ("https://bugcrowd.com/programs")
    bugcrowdReq = requests.get(bugcrowdURL)
    bugcrowdSoup = BeautifulSoup(bugcrowdReq.text)
    bugcrowdPrograms = []
    for programs in bugcrowdSoup.find_all("a", class_="bc-btn bc-btn--small bc-btn--secondary"):
        if (programs.get('href') != '/user/sign_in'):
            program = (programs.get('href'))
            program = program.replace("/report", "")
            program = program.replace("/", "")
            bugcrowdPrograms.append(program)
    recentBugcrowdPrograms = (bugcrowdPrograms[0:5])
    return(recentBugcrowdPrograms)

### Get HackerOne Programs
def HackerOnePrograms():
    hackerOneURL = ("https://hackerone.com/programs/search.json?query=type%3Ahackerone&sort=published_at%3Adescending&page=1&limit=10")
    hackerOneReq = requests.get(hackerOneURL)
    hackerOnePrograms = []
    hackerOneProgramResJSON = json.loads(hackerOneReq.text)
    for hackerOneResult in (hackerOneProgramResJSON['results']):
        hackerOnePrograms.append(hackerOneResult['name'])
    recentHackerOnePrograms = (hackerOnePrograms[0:5])
    return(recentHackerOnePrograms)

### Get HackerOne Hacktivity
def HackerOneHacktivity():
    hackerOneHacktivityURL = ("https://hackerone.com/hacktivity?page=1&filter=public&format=json&limit=10")
    hackerOneHacktivityReq = requests.get(hackerOneHacktivityURL)
    hackerOneHacktivity= []
    hackerOneHacktivityResJSON = json.loads(hackerOneHacktivityReq.text)
    for hackerOneHacktivityResult in (hackerOneHacktivityResJSON['reports']):
        if (hackerOneHacktivityResult['bounty_disclosed']) == True:
            try:
                hackerOneHacktivity.append(str(hackerOneHacktivityResult['title']) +
                                           " on program " + str(hackerOneHacktivityResult['team']['handle']) +
                                           " reported by user " + str(hackerOneHacktivityResult['reporter']['username']))
            except:
                pass
    recentHackerOneHacktivity = (hackerOneHacktivity[0:5])
    return(recentHackerOneHacktivity)

### Welcome Message
@ask.launch
def start_skill():
    welcome_message = "Greetings Hacker, would you like to hear the newest bug crowd programs, hacker one programs or hacker ones hacktivity reports?"
    return question(welcome_message)

### Return Bugcrowd Programs
@ask.intent("BugcrowdIntent")
def BugcrowdProgramsInit():
    bugcrowdPrograms = BugcrowdPrograms()
    bugcrowdPrograms_msg = 'The most recent Bug Crowd programs are {}'.format(bugcrowdPrograms)
    return statement(bugcrowdPrograms_msg)

### Return HackerOne Programs
@ask.intent("HackerOneIntent")
def hackerOneProgramsInit():
    hackerOnePrograms = HackerOnePrograms()
    hackerOnePrograms_msg = 'The most recent Hacker One programs are {}'.format(hackerOnePrograms)
    return statement(hackerOnePrograms_msg)

### Return HackerOne Hacktivity
@ask.intent("HacktivityIntent")
def hacktivityIntent():
    hackerOneHacktivity = HackerOneHacktivity()
    hackerOneHacktivity_msg = 'The most recent Hacker One Hacktivity reports are {}'.format(hackerOneHacktivity)
    return statement(hackerOneHacktivity_msg)

### Amazon Help Intent
@ask.intent('AMAZON.HelpIntent')
def help():
    helpText = "You can ask bug bounty to tell you the newest Bug Crowd programs, newest Hacker One programs or latest Hacker One hacktivity repots."
    return question(helpText).reprompt(helpText)

### Amazon Stop Intent
@ask.intent('AMAZON.StopIntent')
def stop():
    stopText = "Bug bounty also known as the Gibson shutting down."
    return statement(stopText)

### Amazon Cancel Intent
@ask.intent('AMAZON.CancelIntent')
def cancel():
    cancelText = "Bug bounty canceled, Joshua"
    return statement(cancelText)

if __name__ == '__main__':
    app.run(debug=False)
