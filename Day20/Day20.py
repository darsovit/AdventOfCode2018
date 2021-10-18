#!python
'''
Advent of Code 2018, Day 20
https://adventofcode.com/2018/day/20
'''
from collections import deque

def readInput():
    with open('input.txt') as f:
        for line in f:
            return line.rstrip()

def tests():
    return [
        ( '^WNE$', 3 ),
        ( '^ENWWW(NEEE|SSE(EE|N))', 10 ),
        ( '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', 18 ),
        ( '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', 23 ),
        ( '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', 31 )
    ]


def oppositeDir( dir ):
    if dir == 'N':
        return 'S'
    elif dir == 'S':
        return 'N'
    elif dir == 'E':
        return 'W'
    elif dir == 'W':
        return 'E'        
        
#class stringPart:
#    def __init__( self, input ):
        
#def calculateLongestString( input ):
#    length = 0
#    strings = deque()
#    for x in len(input):
        
            
#def sampleInput():
#    return "^ENWWW(NEEE|SSE(EE|N))$"

#def sampleRooms():
#    return [
#        '#########',
#        '#.|.|.|.#',
#        '#-#######',
#        '#.|.|.|.#',
#        '#-#####-#',
#        '#.#.#X|.#',
#        '#-#-#####',
#        '#.|.|.|.#',
#        '#########'
#    ]

class room:
    def __init__( self, distance, exit, exitDir, marker='.' ):
        self.distance = distance
        self.exits = {}
        if exit:
            self.exits[exitDir] = exit
    def updateExit( self, exitDir, distance ):
        if distance < self.distance:
            self.distance = distance
            for dir in self.exits:
                if not dir == exitDir:
                    self.exits[dir].updateExit( oppositeDir( dir ), distance + 1 )
              
    def addExit( self, exit, exitDir, distance ):        
        if distance < self.distance:
            self.distance = distance
            for dir in self.exits:
                if not dir == exitDir:
                    self.exits[dir].updateExit( oppositeDir( dir ), distance + 1 )
        elif distance > self.distance:
            exit.updateExit( oppositeDir( exitDir ), self.distance+1 )
        if exitDir not in self.exits:
            self.exits[exitDir] = exit
        else:
            assert self.exits[exitDir] == exit
        return self.distance

    def getDistance( self ):
        return self.distance

class roomMap:
    def __init__(self, expression):
        self.expression = expression
        self.field = {}
        self.field[(0,0)] = room( 0, None, None, marker='X' )
        self.minHeight = 0
        self.maxHeight = 0
        self.minWidth  = 0
        self.maxWidth  = 0
        
    def buildRoomMap(self):
        conditionDepth = 0
        conditionPos = deque()
        pos = (0,0)
        distanceFromStart = 0
        nextStartPosList = []
        nextStartPosList.append([(0,0)])
        directionDetails = { 'N': {'opposite': 'S', 'posAdjust': (-1,0)},
                             'S': {'opposite': 'N', 'posAdjust': (1,0) },
                             'E': {'opposite': 'W', 'posAdjust': (0,1) },
                             'W': {'opposite': 'E', 'posAdjust': (0,-1)} }
        def adjustPos( curPos, dir ):
            adjustment = directionDetails[dir]['posAdjust']
            return (curPos[0]+adjustment[0], curPos[1]+adjustment[1])

        for character in self.expression:
            if character == '^':
                assert pos == (0,0)
                assert conditionDepth == 0
            elif character == '$':
                assert conditionDepth == 0
            elif character == '(':
                conditionDepth += 1
                conditionPos.append( pos )
            elif character == ')':
                assert conditionDepth > 0
                pos = conditionPos.pop()
                conditionDepth -= 1
                distanceFromStart = self.field[pos].getDistance()

            elif character == '|':
                assert conditionDepth > 0
                pos = conditionPos[-1]
                distanceFromStart = self.field[pos].getDistance()

            else:
                assert character in {'N','S','E','W'}
                direction = character
                
                newDistance = distanceFromStart + 1
                newPos = adjustPos( pos, direction )
                oppositeDir = directionDetails[direction]['opposite']
                if newPos in self.field:
                    newDistance = self.field[newPos].addExit( self.field[pos], oppositeDir, distanceFromStart + 1)
                else:
                    self.field[newPos] = room( distanceFromStart + 1, oppositeDir, self.field[(pos)] )
                    newDistance = distanceFromStart + 1
                self.field[pos].addExit( self.field[newPos], direction, distanceFromStart)
                pos = newPos
                distanceFromStart = newDistance   

    def findFurthestRoom(self):
        distance = 0
        furthestPos = None
        for pos in self.field:
            if self.field[pos].getDistance() > distance:
                distance = self.field[pos].getDistance()
                furthestPos = pos
        return (distance, furthestPos)

for test in tests():
    myMap = roomMap( test[0] )
    myMap.buildRoomMap()
    (result, resultPos) = myMap.findFurthestRoom()
    assert result == test[1]

myMap = roomMap( readInput() )
myMap.buildRoomMap()
print(myMap.findFurthestRoom())