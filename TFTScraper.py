import requests
import re
import timeit
import pandas as pd
from bs4 import BeautifulSoup

default_url = "https://lolchess.gg"
currSeason = "s2"

def getURL(region, username):
    return default_url + "/profile/" + region.lower() + "/" + username

def getURLPrompt():
    region = input("What is your region?")
    username = input("What is your username?")
    
    currURL = default_url + "/profile/" + region.lower() + "/" + username
    return currURL
    
def getAllURL():
    region = input("What is your region?")
    username = input("What is your username?")

    allURL = []
    currURL = default_url + "/profile/" + region + "/" + username + "/" + currSeason + "/matches/all/0"

    for n in range(1, 6): #1-5
        if(not region and not username): #empty use default
            currURL = currURL[:len(currURL)-1] + str(n)
        else:
            currURL = currURL[:len(currURL)-1] + str(n)
        allURL.append(currURL)
    return allURL
    
def getParser(link:str):
    result = requests.get(link)
    parser = BeautifulSoup(result.text, 'html.parser')
    return parser

def getPlacement(currGame):
    placement = int(re.sub("[^0-9]","",currGame.find("div","placement").text))
    return placement
    
def getLevel(currGame):
    level = int(currGame.find("span", "level").text)
    return level

def getTraits(currGame):
    traits = currGame.findAll("div",re.compile("tft-hexagon tft-hexagon"))
    comp = []
    for trait in traits:
        comp.append(trait.find("img").get("title"))
    return comp

def getChampions(currGame):
    compUnits = []
    allUnits = currGame.findAll("div", "unit")
    for champion in allUnits:
        currChamp = champion.find("div", re.compile("tft-champion cost"))
        compUnits.append(currChamp.find("img").get("title"))
    return compUnits

def getItems(currGame):
    compItems = []
    allUnits = currGame.findAll("div", "unit")
    for champion in allUnits:
        champItems = []
        championItems = champion.find("ul", "items")
        items = championItems.findAll("img")
        for item in items: #champion can have multiple items 0-3
            champItems.append(item.get("title")) #individual champ items
        compItems.append(champItems) #all champs items
    return compItems

def placements(placements):
    places = []
    total = 0
    top = 0
    games = len(placements)
    
    for i in range(9):
        places.append(0)

    for n in placements:
        total += n
        places[n] = places[n] + 1
        if n <= 4:
            top = top + 1
    return total/games, top, places, games
        
def allData(placement, level, traits, units, items):
    data = pd.DataFrame({"Placement": placement, "Level": level, "Traits": traits, "Units": units, "Items": items})
    return data

def lastNGames(data, nGames):
    return data.head(int(nGames))
