'''
This is the module for generating tournament schedules. It contains the following functions:
    valid - Tests if a pairing is valid given a list of pairings
    validMatches - Gets all possible valid matches from a competitor, taking into account all previous matches
    generateRound - Generates a round given all previous matches, uses a greedy algorithm.
    generateTournamentSchedule - Generates a list of rounds using generateRound
'''
import math

def valid(newPairing, allPairings):
    """Tests if a pairing is valid when taking into account all other pairings.
    
    If a given tuple is present in a list of all previous pairings (regardless of order), then 
    this function returns false. In context for our tournament code, this is to ensure that no 
    repeated matchups occur. The order of the competitors in a matchup does not matter, so neither should
    our tuple pairing.

    
    :param newPairing: A potential pairing.
    :type param1: tuple
    :param allPairings: All previous pairings
    :type param2: list[tuple]
    """
    a,b = newPairing
    if a == b:
        return False
    if (a,b) in allPairings:
        return False
    if (b,a) in allPairings:
        return False
    return True

def validMatches(competitor, allCompetitors, allMatches):
    validMatches = []
    for cj in allCompetitors:
        possibleMatch = (competitor, cj)
        if valid(possibleMatch,allMatches):
            validMatches.append(possibleMatch)
        else:
            continue
    return validMatches

def generateRound(competitorList,pastPairings,n,partialRound=[],):
    #Warning: Must add Bye before competitor List
    assert len(competitorList) % 2 == 0
    matches = n // 2
    if len(partialRound) == matches:
        #If the number of matches is equal to the number of partial rounds, then we have the desired number of matches
        return partialRound
    else:
        #Get our available competitors.
        availableCompetitors = competitorList.copy()
        pastAndCurrent = pastPairings + partialRound
        #For each competitor...
        for ci in competitorList:
            #Remove our competitor.
            availableCompetitors.remove(ci)
            #Check for valid matches.
            potentialMatches = validMatches(ci,availableCompetitors,pastAndCurrent)
            #If the list of valid matches is 0, then we can't do anything.
            if len(potentialMatches) == 0:
                return None
            #For each match
            else:
                #Try the match.
                for match in potentialMatches:
                    _, cj = match
                    #Remove the cj.
                    availableCompetitors.remove(cj)
                    #Then perform the function on our available competitors, add our past pairings, and our new match.
                    round = generateRound(availableCompetitors, pastPairings, n, partialRound + [match])
                    #If that recursed function is not None, then return the round, since we have a viable round.
                    if round is not None:
                        return round
                    else:
                        #No matches resulted in anything. 
                        availableCompetitors.append(cj)
            availableCompetitors.append(ci)
    #We couldn't find any proper competitors. Return nothing.
    return None


def generateTournamentSchedule(competitorList,n, allPairings = [], fullSchedule = [], rounds = 0):
    '''
    Docstring for generateTournamentSchedule
    
    :param competitorList: List of competitors
    allMatchups = []
    For m = ceil(log2(n))
        
    '''

    assert n % 2 == 0
    numRounds = math.ceil(math.log2(n))
    if rounds == numRounds:
        return fullSchedule
    else:
        round = generateRound(competitorList, allPairings, n)
        if round is None:
            return None
        else:
            fullSchedule.append(round)
            allPairings.extend(round)
            return generateTournamentSchedule(competitorList,n,allPairings,fullSchedule,rounds+1)


