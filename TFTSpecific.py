import re
import TFTScraper


def main():
    finalPlacement = []
    finalLevel = []
    finalTraits = []
    finalUnits = []
    finalItems = []

    region = input("What is your region?")
    username = input("What is your username?")
    
    allURL = TFTScraper.getAllURL(region, username)
    for url in allURL:
        soup = TFTScraper.getParser(url)
        games = soup.findAll("div",re.compile("profile__match-history-v2__item placement-"))

        for game in games:
            finalPlacement.append(TFTScraper.getPlacement(game))
            finalLevel.append(TFTScraper.getLevel(game))
            finalTraits.append(TFTScraper.getTraits(game))
            finalUnits.append(TFTScraper.getChampions(game))
            finalItems.append(TFTScraper.getItems(game))


    ##print data to console and csv file for any extra uses
    allData = TFTScraper.allData(finalPlacement, finalLevel, finalTraits, finalUnits, finalItems)
    if(allData.empty): #there is no error message for invalid usernames
        print("Username does not exist")
    else: #shorten the data
        nGames = input("How many games do you want to know the stats of?")
        shortenedData = TFTScraper.lastNGames(allData, nGames)
        print(shortenedData)

        average, topFours, places, games = TFTScraper.placements(shortenedData['Placement'])
        print("Average placement " + str(average) + " in " + str(games) + " games")
        print("Top four " + str(topFours) + " of " + str(games) + " games")
        for n in range(1,9):
            print(str(places[n]) + " games in " + str(n) + " place")
    
if __name__ == "__main__":
    main()
