import requests
from bs4 import BeautifulSoup
import dryscrape
from threading import Thread


### Bugcrowd Programs
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
    print(bugcrowdPrograms[0:5])

### HackerOne Programs
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
    print(hackerOnePrograms[0:5])


Thread(target=HackerOnePrograms).start()
Thread(target=BugcrowdPrograms).start()