#!python
'''
Advent of Code 2018, Day 9, Problem 1
https://adventofcode.com/2018/day/9
'''

from collections import deque

def getInput():
    with open('input.txt') as f:
        for line in f:
            parts = line.split()
            return ( int(parts[0]), int(parts[6]) )

def playGame( numPlayers, highMarbleScore ):
    field = deque()
    field.append(0)
    field.append(1)
    playerScores = {}
    #print(field)
    for i in range(2,highMarbleScore+1):
        if i % 23 == 0:
            field.rotate(7)
            value = i + field.pop()
            field.rotate(-1)
            playerValue = i % numPlayers
            if playerValue in playerScores:
                playerScores[playerValue] += value
            else:
                playerScores[playerValue] = value
        else:
            field.rotate(-1)
            field.append(i)
        #print(field)
    return playerScores

#playGame(9, 25)
#playGame(10, 1618)
#playGame(13, 7999)


(players, highMarble) = getInput()
# For Part 2
#highMarble *= 100
scores = playGame(players, highMarble)
#print(scores)

highScore = 0
for score in scores:
    if scores[score] > highScore:
        highScore = scores[score]
print(highScore)

