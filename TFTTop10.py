import re
import TFTScraper

def getTopInformation():
    region = []
    username = []
    
    url = "https://lolchess.gg"
    soup = TFTScraper.getParser(url)
    top = soup.find("table", "table frontpage-global-ranking__table")
    topPlayers = top.findAll("tr")
    for n in range(1, 11):
        player = topPlayers[n]
        region.append(player.find("td", "region").text)
        username.append(player.find("a").text.strip())
    return region, username
    
def main():
    regions, usernames = getTopInformation()
    overallUnitCount = dict()
    for n in range(len(usernames)):
        currUnitCount = dict()
        finalPlacement = []
        finalLevel = []
        finalTraits = []
        finalUnits = []
        finalItems = []

        currRegion = regions[n]
        currUsername = usernames[n]
        
        link = TFTScraper.getURL(currRegion, currUsername)
        soup = TFTScraper.getParser(link)

        games = soup.findAll("div",re.compile("profile__match-history-v2__item placement-"))

        for game in games:
                finalPlacement.append(TFTScraper.getPlacement(game))
                finalLevel.append(TFTScraper.getLevel(game))
                finalTraits.append(TFTScraper.getTraits(game))
                finalItems.append(TFTScraper.getItems(game))
                
                finalUnits.append(TFTScraper.getChampions(game))
                for unit in TFTScraper.getChampions(game):
                    if unit in overallUnitCount:
                        overallUnitCount[unit] += 1
                    else:
                        overallUnitCount[unit] = 1
                    if unit in currUnitCount:
                        currUnitCount[unit] += 1
                    else:
                        currUnitCount[unit] = 1
                        
        allData = TFTScraper.allData(finalPlacement, finalLevel, finalTraits, finalUnits, finalItems)
        
        average, topFours, places, games = TFTScraper.placements(allData['Placement'])

        print("Rank #" + str(n+1) + " " + str(currUsername) + " ending stats")
        print("Average placement " + str(average) + " in last " + str(games) + " games")
        print("Top four " + str(topFours) + " of last " + str(games) + " games")
        for i in range(1,9):
            print(str(places[i]) + " games in " + str(i) + " place")

        allData.to_csv("#" + str(n+1) + " " + str(currUsername) + ".csv")

        print(sorted(currUnitCount.items(), key=lambda x: x[1], reverse = True))
        print()
    print(sorted(overallUnitCount.items(), key=lambda x: x[1], reverse = True))
if __name__ == "__main__":
    main()
