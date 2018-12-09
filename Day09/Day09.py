#!python
'''
Advent of Code 2018, Day 9, Problem 1
https://adventofcode.com/2018/day/9
'''

def getInput():
    with open('input.txt') as f:
        for line in f:
            parts = line.split()
            return ( int(parts[0]), int(parts[6]) )

def playGame( numPlayers, highMarbleScore ):
    field = [ 0 ]
    currentPos = 0
    playerScores = {}
    #print(field,currentPos)
    for i in range(1,highMarbleScore+1):
        if i % 23 == 0:
            removalPos = (currentPos - 7) % len(field)
            value = i + field[removalPos]
            field = field[:removalPos] + field[removalPos+1:]
            currentPos = removalPos
            playerValue = i % numPlayers
            if playerValue in playerScores:
                playerScores[playerValue] += value
            else:
                playerScores[playerValue] = value
        else:
            placementPos = ( currentPos + 2 ) % (len(field))
            field = field[:placementPos] + [i] + field[placementPos:]
            currentPos = placementPos
        #print(field, currentPos)
    return playerScores

playGame(9, 25)
playGame(10, 1618)
playGame(13, 7999)

(players, highMarble) = getInput()
scores = playGame(players, highMarble*100)

highScore = 0
for score in scores:
    if scores[score] > highScore:
        highScore = scores[score]
print(highScore)

