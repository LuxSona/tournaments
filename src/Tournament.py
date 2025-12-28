'''Tournament logic, including matchups and the Swiss Tournament system

:function userConfirmation: Prompts the user to adjucate a matchup.
'''
from elo import Competitor, Bye, calculateElo
from random import shuffle
import math
from RoundGenerator import generateTournamentSchedule


def userConfirmation(matchup, leftTitle = "l", rightTitle = "r", drawTitle = "d"):
    '''Ask the user to adjucate a matchup using CLI.

    This function takes a matchup and title characters. It then prompts the user for the matchup.
    Handles Byes. 

    
    :param matchup: The matchup to adjucate.
    :param leftTitle: The title of the left competitor.
    :param rightTitle: The title of the right competitor.
    :param drawTitle: The title of the drawing option.
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
    '''Matchup class which holds logic for a matchup between two Competitors.

    This class holds the logic for two Competitor objects to face off against each other.
    Will allow for setting the outcome and getting names.

    :param lc: Left competitor
    :type lc: Competitor
    :param rc: Right competitor
    :type rc: Competitor
    '''
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
        '''Sets the outcome for the matchup

        This function sets the outcome for the matchup. Preferred 0s and 1 for wins and losses.

        :param lcscore: The score for the left competitor. Int
        :param rcscore: The score for the right competitor. Int
        '''
        #Set the outcome by calculating elo
        ls, rs = calculateElo(self.lc, self.rc, lcScore, rcScore)
        print(ls,rs)
        #Set ratings
        self.lc.setRating(ls)
        self.rc.setRating(rs)
        #Update result
        self.result = (lcScore, rcScore)
    
    def getNames(self):
        '''Gets the names of the left and right competitors,
        '''
        #Return names
        return self.lc.name, self.rc.name

    def __repr__(self):
        #Representation
        return str((self.lc.name, self.rc.name, self.result))

class SwissTournament():
    '''Swiss torunament logic.

    This class holds the logic for a Swiss style tournament.
    :param competitors: A list of competitors. Either in name form (if string mode is enabled) or in object form.
    :type competitors: List[Competitor] or List[String]
    :param stringMode: Whether or not the Swiss tournament should treat the competitor list as a list of strings or list of Competitor objects.
    :type stringMode: bool
    '''
    def __init__(self, competitors, stringMode = False):
        if (stringMode):
            competitors = list(map(Competitor, competitors))
        
        if len(competitors) % 2 != 0:
            competitors.append(Bye("Bye"))
        self.n = len(competitors)
        self.competitors = competitors
    
    def generateSchedule(self):
        '''Generate schedule
        
        This function uses our roundGenerator module to generate a full match schedule.
        '''
        tempSchedule = generateTournamentSchedule(self.competitors,self.n)
        self.schedule = [[Matchup(lc,rc) for (lc, rc) in inner] for inner in tempSchedule]
        return self.schedule
    
    def holdAllRounds(self):
        '''Hold all rounds
        
        Will generate the schedule, then hold all rounds within the schedule.
        '''
        self.generateSchedule()
        i = 0
        for round in self.schedule:
            print(f"Round {i+1}")
            for matchup in round:
                userConfirmation(matchup)
            i+=1
    
    def showAllStandings(self):
        '''Shows all standings

        This function prints to stdout the standings of all the competitors.
        '''
        #Sort competitors by elo
        self.competitors.sort(key=lambda comp: comp.getRating(),reverse=True)
        reversed(self.competitors)
        print("Here are the standings!")
        for competitor in self.competitors:
            print(competitor.name, "---", competitor.getRating())
    
    def getAllMatches(self):
        '''Retrieves all matches.

        Returns a list of lists, where each sublist represents a single round of play.
        '''
        return self.schedule