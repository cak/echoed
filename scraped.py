import requests
from bs4 import BeautifulSoup
import dryscrape
from threading import Thread
from flask import Flask, render_template
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
    return(bugcrowdPrograms[0:5])

### Get HackerOne Programs
def HackerOnePrograms():
    hackerOneURL = ("https://hackerone.com/directory?query=type%3Ahackerone&sort=published_at%3Adescending&page=1")
    hackerOneReq = requests.get(hackerOneURL)
    hackerOnePrograms = []
    session = dryscrape.Session()
    session.visit(hackerOneURL)
    hackerOneReq = session.body()
    hackerOneSoup = BeautifulSoup(hackerOneReq)
    for programs in hackerOneSoup.find_all("a", class_="leaderboard-user__name spec-profile-name-with-popover"):
        program = (programs.get('href'))
        program = program.replace("/", "")
        hackerOnePrograms.append(program)
    recentHackerOnePrograms = (hackerOnePrograms[0:5])
    return (recentHackerOnePrograms)

### Welcome Message
@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to hear the newest bug bounty programs from bugcrowd, hackerone or both?'
    return question(welcome_message)

### Return Bugcrowd Programs
@ask.intent("BugcrowdIntent")
def BugcrowdProgramsInit():
    bugcrowdPrograms = BugcrowdPrograms()
    bugcrowdPrograms_msg = 'The most recent Bugcrowd programs are {}'.format(bugcrowdPrograms)
    return statement(bugcrowdPrograms_msg)

### Return HackerOne Programs
@ask.intent("HackerOneIntent")
def hackerOneProgramsInit():
    hackerOnePrograms = HackerOnePrograms()
    hackerOnePrograms_msg = 'The most recent HackerOne programs are {}'.format(hackerOnePrograms)
    return statement(hackerOnePrograms_msg)


@ask.intent("BothIntent")
def bothPlatforms():
    return("Both!")

#Thread(target=HackerOnePrograms).start()
#Thread(target=BugcrowdPrograms).start()

if __name__ == '__main__':
    app.run(debug=True)
