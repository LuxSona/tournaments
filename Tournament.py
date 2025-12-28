from elo import Competitor, Bye, calculateElo
from random import shuffle
import math
from roundGenerator import generateTournamentSchedule


def userConfirmation(matchup, leftTitle = "l", rightTitle = "r", drawTitle = "d"):
    '''
    Ask the user to adjucate a matchup using CLI    
    :param matchup: The matchup to adjucate
    '''

    #Get the matchup's competitors
    lc, rc = matchup.getNames()
    print(f"{lc} vs {rc}")
    if matchup.ByeMode:
        print("This one's a bye. We advance forward!")
        return
    print("Who wins?!")
    print(f"{leftTitle} for {lc}, {rightTitle} for {rc}, {drawTitle} for draw.")
    choice = input()
    if choice.lower() == leftTitle:
        winner = lc
        matchup.outcome(1,0)
        print(f"{winner} wins!")
    elif choice.lower() == rightTitle:
        winner = rc
        matchup.outcome(0,1)
        print(f"{winner} wins!")
    else:
        matchup.outcome(0.5,0.5)
        print("It's a draw!")
    
class Matchup():
    def __init__(self, lc, rc):
        #left and right competitors
        self.lc = lc
        self.rc = rc
        #No result yet
        self.result = None
        self.ByeMode = False
        if type(lc) == Bye or type(rc) == Bye:
            self.ByeMode = True
    
    def outcome(self, lcScore, rcScore):
        #Set the outcome by calculating elo
        ls, rs = calculateElo(self.lc, self.rc, lcScore, rcScore)
        print(ls,rs)
        #Set ratings
        self.lc.setRating(ls)
        self.rc.setRating(rs)
        #Update result
        self.result = (lcScore, rcScore)
    
    def getNames(self):
        #Return names
        return self.lc.name, self.rc.name

    def __repr__(self):
        #Representation
        return str((self.lc.name, self.rc.name, self.result))

class SwissTournament():
    def __init__(self, competitors, stringMode = False):
        if (stringMode):
            competitors = list(map(Competitor, competitors))
        
        if len(competitors) % 2 != 0:
            competitors.append(Bye("Bye"))
        self.n = len(competitors)
        self.competitors = competitors
    
    def generateSchedule(self):
        tempSchedule = generateTournamentSchedule(self.competitors,self.n)
        self.schedule = [[Matchup(lc,rc) for (lc, rc) in inner] for inner in tempSchedule]
        return self.schedule
    
    def holdAllRounds(self):
        self.generateSchedule()
        i = 0
        for round in self.schedule:
            print(f"Round {i+1}")
            for matchup in round:
                userConfirmation(matchup)
            i+=1
    
    def showAllStandings(self):
        #Sort competitors by elo
        self.competitors.sort(key=lambda comp: comp.getRating(),reverse=True)
        reversed(self.competitors)
        print("Here are the standings!")
        for competitor in self.competitors:
            print(competitor.name, "---", competitor.getRating())

