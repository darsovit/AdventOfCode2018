#!python
'''
Advent of Code 2018, Day 15
https://adventofcode.com/2018/day/15
'''
from collections import deque

deltasToCheck = [ (-1,0), (0,-1), (0,1), (1,0) ]

def addCoordAndDelta( coord, delta ):
    return ( coord[0]+delta[0], coord[1]+delta[1] )

def getElementAtPos( coord, board ):
    return board[coord[0]][coord[1]]

class unit:
    def __init__(self, goblinOrElf, pos):
        self.state = {}
        self.state['race'] = goblinOrElf
        self.state['hp'] = 200
        self.state['attack'] = 3
        self.state['pos'] = pos
        self.state['enemy'] = 'G' if goblinOrElf == 'E' else 'E'

    def __repr__(self):
        return '{}({})'.format(self.state['race'], self.state['hp'])

    def getHealth(self):
        return self.state['hp']

    def getEnemyRace(self):
        return self.state['enemy']

    def walkSeededBackwardsToGen1( self, startPos, foundEnemy, seeded ):
        storePrior = foundEnemy
        ( prior, gen ) = seeded[foundEnemy]
        while gen > 1:
            storePrior = prior
            (prior, gen) = seeded[storePrior]
        return storePrior

    def nextToEnemy(self, board):
        for delta in deltasToCheck:
            if self.state['enemy'] == getElementAtPos( addCoordAndDelta( self.state['pos'], delta ), board ):
                #print( 'Found adjacent enemy, no need to move:', self.state['pos'], delta )
                return True
        return False

    def findAllEnemyAttackPositions(self, board, unitPositions):
        enemyAttackPositions = set()
        for unitPosition in unitPositions:
            (race,unitId) = unitPositions[unitPosition]
            if race == self.state['enemy']:
                for delta in deltasToCheck:
                    if '.' == getElementAtPos( addCoordAndDelta( unitPosition, delta ), board ):
                        enemyAttackPositions.add( addCoordAndDelta( unitPosition, delta ) )
        listOfAttackPos = list( enemyAttackPositions )
        listOfAttackPos.sort()
        return listOfAttackPos

    def findClosestEnemyAttackPosition(self, board, unitPositions):
        seeded = {}
        startPos = self.state['pos']
        seeded[startPos] = (None, 0)
        
        allAttackPositions = self.findAllEnemyAttackPositions( board, unitPositions )

        seed = []
        seed = [ startPos ]
        foundEnemyAttackPositions = []
        
        while ( len(foundEnemyAttackPositions) == 0 ) and len(seed) > 0:
            nextGenSeeds = []
            for posToTest in seed:
                generation = seeded[posToTest][1]
                for delta in deltasToCheck:
                    nextPos = addCoordAndDelta( posToTest, delta )
                    if nextPos not in seeded:
                        seeded[nextPos] = (posToTest, generation+1)
                        targetVal = getElementAtPos( nextPos, board )
                        if targetVal == '.':
                            nextGenSeeds += [ nextPos ]
                        elif targetVal == self.state['enemy']:
                            foundEnemyAttackPositions.append( posToTest )
            seed = nextGenSeeds
        #
        
        if len(foundEnemyAttackPositions) == 0:
            #print( self, ", no found enemy attack positions." )
            return startPos
        foundEnemyAttackPositions.sort()
        (endPos,gen) = seeded[foundEnemyAttackPositions[0]]
        if gen == 1:
            return foundEnemyAttackPositions[0]
        else:
            return self.walkSeededBackwardsToGen1(startPos,foundEnemyAttackPositions[0],seeded)

    def findAdjacentEnemies( self, pos, board, enemyRace ):
        enemies = []
        for delta in deltasToCheck:
            possiblePos = addCoordAndDelta( pos, delta )
            if getElementAtPos( possiblePos, board ) == enemyRace:
                enemies += [ possiblePos ]
        return enemies

    def move(self, pos):
        self.state['pos'] = pos

    def determineNewPos(self, board, unitPositions):
        assert( getElementAtPos(self.state['pos'], board) == self.state['race'] )
        if self.nextToEnemy( board ):
            return (self.state['pos'])
        return self.findClosestEnemyAttackPosition( board, unitPositions )

    def determineEnemiesAvailableToAttack( self, board ):
        (curY,curX) = self.state['pos']
        assert( board[curY][curX]  == self.state['race'] )
        return ( self.findAdjacentEnemies( self.state['pos'], board, self.state['enemy'] ), self.state['attack'] )

    def takeDamage( self, dmg ):
        self.state['hp'] -= dmg
        return self.state['hp'] > 0
    
class bandits:
    def __init__(self, lines):
        self.state = {}
        self.state['board'] = []
        self.state['units'] = {}
        self.state['units']['G'] = {}
        self.state['units']['E']   = {}
        self.state['unitPos'] = {}
        self.state['numRounds'] = 0

        self.parseLines(lines)
        
    def parseLines(self, lines):
        squadNo = 1
        for y in range(len(lines)):
            self.state['board'] += [ lines[y] ]
            for x in range(len(lines[y])):
                if 'G' == lines[y][x]:
                    self.state['units']['G'][squadNo] = unit('G',(y,x))
                    self.state['unitPos'][(y,x)] = ('G',squadNo)
                    squadNo += 1
                elif 'E' == lines[y][x]:
                    self.state['units']['E'][squadNo] = unit('E',(y,x))
                    self.state['unitPos'][(y,x)] = ('E',squadNo)
                    squadNo += 1

    def removeSquadFromBoard( self, oldPos ):
        lineToChange = self.state['board'][oldPos[0]]
        newLine = lineToChange[:oldPos[1]] + '.' + lineToChange[oldPos[1]+1:]
        self.state['board'][oldPos[0]] = newLine
        
    def addSquadToBoard( self, newPos, race ):
        lineToChange = self.state['board'][newPos[0]]
        assert( lineToChange[newPos[1]] == '.' )
        newLine = lineToChange[:newPos[1]] + race + lineToChange[newPos[1]+1:]
        self.state['board'][newPos[0]] = newLine

    def moveSquad( self, oldPos, newPos ):
        #print( 'Moving from', oldPos, 'to', newPos )
        (race,squadNo) = self.state['unitPos'][oldPos]
        del self.state['unitPos'][oldPos]
        assert( newPos not in self.state['unitPos'] )
        self.state['unitPos'][newPos] = (race,squadNo)
        self.state['units'][race][squadNo].move(newPos)
        self.removeSquadFromBoard( oldPos )
        self.addSquadToBoard( newPos, race )

    def debugPrint(self):
        print('Num Rounds:', self.state['numRounds'] )
        for line in self.state['board']:
            print( line )
        for elfPos in self.state['units']['E']:
            print( elfPos, self.state['units']['E'][elfPos] )
        for goblinPos in self.state['units']['G']:
            print( goblinPos, self.state['units']['G'][goblinPos] )

    def removeUnit( self, pos ):
        (race,squadNo) = self.state['unitPos'][pos]
        del self.state['units'][race][squadNo]
        del self.state['unitPos'][pos]
        self.removeSquadFromBoard( pos )

    def findTargetHpUnit( self, units ):
        lowestHp = None
        lowestEnemy = []
        for unit in units:
            (race,squadNo) = self.state['unitPos'][unit]
            unitHp = self.state['units'][race][squadNo].getHealth()
            if not lowestHp:
                lowestHp = unitHp
                lowestEnemy = [ unit ]
            elif unitHp < lowestHp:
                lowestHp = unitHp
                lowestEnemy = [ unit ]
            elif unitHp == lowestHp:
                lowestEnemy += [ unit ]
        if not lowestHp:
            return None
        if len( lowestEnemy ) > 1:
            lowestEnemy.sort()
        return lowestEnemy[0]
              
    def performCompleteRound(self):
        unitOrder = list( self.state['unitPos'].keys() )
        unitOrder.sort()
        #print( unitOrder )
        ensureSameUnit = {}
        for unitPos in unitOrder:
            ensureSameUnit[unitPos] = self.state['unitPos'][unitPos]
        for unitPos in unitOrder:
            if unitPos in self.state['unitPos'] and ensureSameUnit[unitPos] == self.state['unitPos'][unitPos]:
                (race,squadNo) = self.state['unitPos'][unitPos]
                if len( self.state['units'][self.state['units'][race][squadNo].getEnemyRace()] ) == 0:
                    return True
                #print( unitPos, race, squadNo )
                if squadNo in self.state['units'][race]:
                    # Move action
                    pos = self.state['units'][race][squadNo].determineNewPos(self.state['board'], self.state['unitPos'])
                    if not ( pos == unitPos ):
                        self.moveSquad(unitPos, pos)
                    # Attack action
                    ( enemiesAvailable, dmg ) = self.state['units'][race][squadNo].determineEnemiesAvailableToAttack(self.state['board'])
                    enemyToAttack = self.findTargetHpUnit( enemiesAvailable )
                    if enemyToAttack:
                        (enemyRace,enemySquad) = self.state['unitPos'][enemyToAttack]
                        alive = self.state['units'][enemyRace][enemySquad].takeDamage( dmg )
                        if not alive:
                            self.removeUnit(enemyToAttack)
            elif unitPos in self.state['unitPos'] and ensureSameUnit[unitPos] != self.state['unitPos'][unitPos]:
                print( 'Unit in pos is now different from original:', unitPos, ensureSameUnit[unitPos], self.state['unitPos'][unitPos] )
            else:
                #print( 'Failed to find ', unitPos, ' in unitPos dict():', self.state['unitPos'] )
                continue
        self.state['numRounds'] += 1
        return False

    def calculateValue(self):
        remainingHealth = 0
        for unit in self.state['unitPos']:
            (race,squadNo) = self.state['unitPos'][unit]
            remainingHealth += self.state['units'][race][squadNo].getHealth()
        print( remainingHealth, self.state['numRounds'], remainingHealth * self.state['numRounds'] )
        return remainingHealth * self.state['numRounds']
        
def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )
        
def testInput1():
    return ( [
        '#######',
        '#.G...#', #   G(200)
        '#...EG#', #   E(200), G(200)
        '#.#.#G#', #   G(200)
        '#..G#E#', #   G(200), E(200)
        '#.....#',
        '#######'
    ], 27730 )

def testInput2():
    return ( [
        '#######',       #######
        '#G..#E#',       #...#E#   E(200)
        '#E#E.E#',       #E#...#   E(197)
        '#G.##.#', #-->  #.E##.#   E(185)
        '#...#E#',       #E..#E#   E(200), E(200)
        '#...E.#',       #.....#
        '#######'        #######
    ], 36334 )

def testInput3():
    return ( [
        '#######',       #######   
        '#E..EG#',       #.E.E.#   E(164), E(197)
        '#.#G.E#',       #.#E..#   E(200)
        '#E.##E#', #-->  #E.##.#   E(98)
        '#G..#.#',       #.E.#.#   E(200)
        '#..E#.#',       #...#.#   
        '#######'        #######   
    ], 39514 )

def testInput4():
    return ([
        '#######',       #######   
        '#E.G#.#',       #G.G#.#   G(200), G(98)
        '#.#G..#',       #.#G..#   G(200)
        '#G.#.G#', #-->  #..#..#   
        '#G..#.#',       #...#G#   G(95)
        '#...E.#',       #...G.#   G(200)
        '#######'        #######   
    ], 27755 )
    
def testInput5():
    return([
        '#######',       #######   
        '#.E...#',       #.....#   
        '#.#..G#',       #.#G..#   G(200)
        '#.###.#', #-->  #.###.#   
        '#E#G#G#',       #.#.#.#   
        '#...#G#',       #G.G#G#   G(98), G(38), G(200)
        '#######'        #######   
    ], 28944 )
    
def testInput6():
    return([
        '#########',       #########   
        '#G......#',       #.G.....#   G(137)
        '#.E.#...#',       #G.G#...#   G(200), G(200)
        '#..##..G#',       #.G##...#   G(200)
        '#...##..#', #-->  #...##..#   
        '#...#...#',       #.G.#...#   G(200)
        '#.G...G.#',       #.......#   
        '#.....G.#',       #.......#   
        '#########'        #########   
    ], 18740)

def playGame( game ):
    done = False
    while not done:
        done = game.performCompleteRound()
        #game.debugPrint()
    game.debugPrint()

def testGame( input, inputName ):
    ( lines, expectedResult ) = input
    game = bandits(lines)
    playGame( game )
    #done = False
    #while not done:
    #    done = game.performCompleteRound()
    #game.debugPrint()
    gameValue = game.calculateValue()
    print( gameValue, expectedResult )
    assert expectedResult == game.calculateValue()
    

#testGame( testInput1(), "input 1" )
#testGame( testInput2(), "input 2" )
#testGame( testInput3(), "input 3" )
#testGame( testInput4(), "input 4" )
#testGame( testInput5(), "input 5" )
#testGame( testInput6(), "input 6" )

game = bandits( readInput() )
playGame( game )
print( game.calculateValue() )

# 209200 is too high for real input