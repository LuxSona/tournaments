import numpy as np

'''
Implementation of the ELO rating system for ranking arbitrary objects.
Competitor class represents an entity with a name and a list of scores.
'''


class Competitor:
    def __init__(self, name):
        self.name = name
        self.rating = 1500
    
    def getRating(self):
        return self.rating

    def setRating(self, new_rating):
        self.rating = new_rating

class Bye(Competitor):
    def __init__(self, name):
        super().__init__(name)
        self.rating = 0
    

def getProbability(rating_a, rating_b):
    return 1.0 / (1 + 10 ** ((rating_b - rating_a) / 400))

def calculateElo(left, right, leftScore, rightScore, k=32):
    leftRating = left.getRating()
    rightRating = right.getRating()
    
    probLeft = getProbability(leftRating, rightRating)
    probRight = getProbability(rightRating, leftRating)
    

    
    leftRatingA = leftRating + k * (leftScore - probLeft)
    rightRatingA = rightRating + k * (rightScore - probRight)
    
    return leftRatingA, rightRatingA


def main():
    n = 5
    a = Bye("Bye 1")
    print(a.getRating())
if __name__ == "__main__":
    main()
    