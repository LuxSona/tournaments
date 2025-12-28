'''
Implementation of the ELO rating system for ranking arbitrary objects.
Competitor class represents an entity with a name and a list of scores.
'''

import numpy as np
class Competitor:
    '''Competitor logic. Holds an elo rating.

    :param name: The name of the competitor/
    '''
    def __init__(self, name):
        self.name = name
        self.rating = 1500
    
    def getRating(self):
        '''Returns rating
        '''
        return self.rating

    def setRating(self, new_rating):
        '''Sets the rating
        '''
        self.rating = new_rating

class Bye(Competitor):
    ''' Bye class. Inherits from the competitor. Sets the rating to 0.
    '''
    def __init__(self, name):
        super().__init__(name)
        self.rating = 0
    

def getProbability(rating_a, rating_b):
    '''Returns the probability of rating a winning against rating b.

    :param rating_a: The rating of the first competitor.
    :param rating_b: The rating of the second competitor.
    '''
    return 1.0 / (1 + 10 ** ((rating_b - rating_a) / 400))

def calculateElo(left, right, leftScore, rightScore, k=32):
    '''Approximates the accurate elo rating given our probability function and an empirical outcome.

    :param left: The left competitor.
    :type left: Competitor
    :param right: the right competitor.
    :type right: Competitor
    :param leftScore: The score for the left competitor.
    :param rightscore: the score for the right competitor.
    :param k: the k value. Default is 32. 
    '''
    leftRating = left.getRating()
    rightRating = right.getRating()
    
    probLeft = getProbability(leftRating, rightRating)
    probRight = getProbability(rightRating, leftRating)
    

    
    leftRatingA = leftRating + k * (leftScore - probLeft)
    rightRatingA = rightRating + k * (rightScore - probRight)
    
    return leftRatingA, rightRatingA


