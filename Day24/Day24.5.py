#! python
'''
Advent of Code 2018, Day 24, Part 1
https://adventofcode.com/2018/day/24
'''
import re

exprWithAdditional = re.compile( r'^(?P<numUnit>\d+) units each with (?P<hp>\d+) hit points \((?P<addl>.*)\) with an attack that does (?P<dmg>\d+) (?P<dmgType>\w+) damage at initiative (?P<initiative>\d+)' )
exprWithoutAdditional = re.compile( r'^(?P<numUnit>\d+) units each with (?P<hp>\d+) hit points with an attack that does (?P<dmg>\d+) (?P<dmgType>\w+) damage at initiative (?P<initiative>\d+)' )

def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )
        
def test1():
    return ( [
        'Immune System:',
        '17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2',
        '989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3',
        '',
        'Infection:',
        '801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1',
        '4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4' 
    ], 5216 )

def sampleInput():
    (lines,expectedOutput) = test1()
    return lines

class squadron:
    def __init__( self, groupNo, numUnits, hpPerUnit, dmg, dmgType, initiative, immune_types, weak_types ):
        self.groupNo      = groupNo
        self.numUnits     = numUnits
        self.hpPerUnit    = hpPerUnit
        self.dmg          = dmg
        self.dmgType      = dmgType
        self.initiative   = initiative
        self.immune_types = immune_types
        self.weak_types   = weak_types
    
    def getEffectivePower(self):
        return self.dmg * self.numUnits

    def getInitiative( self ):
        return self.initiative
        
    def getDamageType( self ):
        return self.dmgType
    
    def getDamageAgainst( self, effectivePowerOfAttacker, dmgTypeOfAttacker ):
        if dmgTypeOfAttacker in self.immune_types:
            return 0
        elif dmgTypeOfAttacker in self.weak_types:
            return 2 * effectivePowerOfAttacker
        else:
            return effectivePowerOfAttacker

    def takeDamage( self, effectivePowerOfAttacker, dmgTypeOfAttacker ):
        totalDmg = self.getDamageAgainst( effectivePowerOfAttacker, dmgTypeOfAttacker )
        numUnitsDestroyed = int( totalDmg / self.hpPerUnit )
        if numUnitsDestroyed > self.numUnits:
            numUnitsDestroyed = self.numUnits
            self.numUnits = 0
        else:
            self.numUnits -= numUnitsDestroyed
        return numUnitsDestroyed

    def getNumUnits( self ):
        return self.numUnits

    def __repr__( self ):
        return str(self.__class__) + ': ' + str(self.__dict__)
        
def buildSquadron( groupNo, line, addedDmg ):
    additional = False
    regex_match = exprWithAdditional.match( line )
    if regex_match:
        additional = True
    else:
        regex_match = exprWithoutAdditional.match( line )
    assert regex_match
    numUnits   = int( regex_match.group('numUnit') )
    hpPerUnit  = int( regex_match.group('hp') )
    dmgPerUnit = int( regex_match.group('dmg') ) + addedDmg
    dmgType    = regex_match.group('dmgType')
    initiative = int( regex_match.group('initiative') )
    immune_type = []
    weak_type   = []
    if additional:
        addl_text = regex_match.group('addl')
        split_addl = addl_text.split('; ')
        for types in split_addl:
            break_down = types.split(' ')
            if break_down[0] == 'immune':
                for x in range(2,len(break_down)-1):
                    immune_type += [ break_down[x][:-1] ]
                immune_type += [ break_down[-1] ]
            elif break_down[0] == 'weak':
                for x in range(2,len(break_down)-1):
                    weak_type += [ break_down[x][:-1] ]
                weak_type += [ break_down[-1] ]
    return squadron( groupNo, numUnits, hpPerUnit, dmgPerUnit, dmgType, initiative, immune_type, weak_type )

def dontPrint( *args ):
    while True:
        break

def parseInput( lines, addedPowerForImmune ):
    system = {}
    system['immune'] = {}
    system['infection'] = {}
    system['debug'] = dontPrint
    state = 0
    groupNo = 1
    
    for line in lines:
        if state == 0 and line == 'Immune System:':
            state = 1
        elif state == 1:
            if len(line) == 0:
                state = 2
            else:
                system['immune'][groupNo] = buildSquadron( groupNo, line, addedPowerForImmune )
                groupNo += 1
                    
        elif state == 2 and line == 'Infection:':
            state = 3
            groupNo = 1
        elif state == 3:
            system['infection'][groupNo] = buildSquadron( groupNo, line, 0 )
            groupNo += 1

    assert state == 3
    return system

def getEnemy( type ):
    if type == 'immune':
        return 'infection'
    else:
        assert type == 'infection'
        return 'immune'

def buildTargetSelectionOrder( system ):
    effectivePowerOrder = []
    for squadType in [ 'immune', 'infection' ]:
        for immuneSquadNo in system[squadType]:
            effectivePower = system[squadType][immuneSquadNo].getEffectivePower()
            initiative     = system[squadType][immuneSquadNo].getInitiative()
            effectivePowerOrder.append( ( 0 - effectivePower, 0 - initiative, squadType, immuneSquadNo ) )
    effectivePowerOrder.sort()
    return effectivePowerOrder
    
def performTargetSelection( system ):
    targetSelected = {}
    targetSelectionOrder = buildTargetSelectionOrder( system )
    possibleTargets = {}
    for squadType in [ 'immune', 'infection' ]:
        possibleTargets[squadType] = set()
        for squadNo in system[squadType]:
            possibleTargets[squadType].add( squadNo )
    #print( targetSelectionOrder )
    for squadronInfo in targetSelectionOrder:
        squadType = squadronInfo[2]
        squadNum   = squadronInfo[3]
        effectivePower = system[squadType][squadNum].getEffectivePower()
        dmgType        = system[squadType][squadNum].getDamageType()
        enemy = getEnemy( squadType )
        maxDmg                  = None
        maxDmgAgainstSquad      = None
        defendersEffectivePower = None
        defendersInitiative     = None
        for enemyNo in possibleTargets[enemy]:
            dmgAgainst = system[enemy][enemyNo].getDamageAgainst( effectivePower, dmgType )
            thisEnemyEffectivePower = system[enemy][enemyNo].getEffectivePower()
            thisEnemyInitiative     = system[enemy][enemyNo].getInitiative()
            system['debug']( squadType, 'group', squadNum, 'would deal defending group', enemyNo, dmgAgainst, 'damage' )
            if not maxDmg or dmgAgainst > maxDmg:
                maxDmg = dmgAgainst
                maxDmgAgainstSquad = (enemy,enemyNo)
                defendersEffectivePower = thisEnemyEffectivePower
                defendersInitiative     = thisEnemyInitiative
            elif dmgAgainst == maxDmg and thisEnemyEffectivePower > defendersEffectivePower:
                maxDmgAgainstSquad = (enemy,enemyNo)
                defendersEffectivePower = thisEnemyEffectivePower
                defendersInitiative     = thisEnemyInitiative
            elif dmgAgainst == maxDmg and thisEnemyEffectivePower == defendersEffectivePower and thisEnemyInitiative > defendersInitiative:
                maxDmgAgainstSquad  = (enemy,enemyNo)
                defendersInitiative = thisEnemyInitiative
        if maxDmgAgainstSquad:
            #system['debug']( squadType, 'group', squadNum, 'chooses to attack defending group', maxDmgAgainstSquad )
            possibleTargets[enemy].remove(maxDmgAgainstSquad[1])
            targetSelected[(squadronInfo[1], squadType, squadNum)] = maxDmgAgainstSquad
    return targetSelected
        
def performAttacks( targets, system ):
    sorted_keys = list( targets.keys() )
    sorted_keys.sort()
    numUnitsDestroyed = 0
    for key in sorted_keys:
        target = targets[key]
        attackerPower = None
        attackerDmgType = None
        if key[2] in system[key[1]]:
            attackerPower = system[key[1]][key[2]].getEffectivePower()
            attackerDmgType = system[key[1]][key[2]].getDamageType()
        if target[1] in system[target[0]] and attackerPower:
            thisNumUnitsDestroyed = system[target[0]][target[1]].takeDamage( attackerPower, attackerDmgType )
            system['debug']( key[1], 'group', key[2], 'attacks defending group', target[1], ', killing', thisNumUnitsDestroyed, 'units' )
            numUnitsDestroyed += thisNumUnitsDestroyed
            if system[target[0]][target[1]].getNumUnits() == 0:
                del system[target[0]][target[1]]
    return numUnitsDestroyed

def printDebugStart( system ):
    print('Immune System:')
    for x in system['immune']:
        print( 'Group', x, 'contains', system['immune'][x].getNumUnits(), 'units' )
    print('Infection:')
    for x in system['infection']:
        print( 'Group', x, 'contains', system['infection'][x].getNumUnits(), 'units' )
    print()

def runSimulation( system ):
    done = ( len(system['immune']) == 0 ) or ( len(system['infection']) == 0 )
    while not done:
        if system['debug'] == print:
            printDebugStart( system )
        targets = performTargetSelection( system )
        numUnitsDestroyed = performAttacks( targets, system )
        system['debug']()
        done = ( len( system['immune'] ) == 0 ) or ( len( system['infection'] ) == 0 ) or ( numUnitsDestroyed == 0 )

def countNumWinningUnits( system ):
    winners = None
    if len(system['immune']) > 0 and len(system['infection']) > 0:
        return ( 'draw', 0 )
    if len(system['immune']) > 0:
        assert len(system['infection']) == 0
        winners = 'immune'
    else:
        assert len(system['immune']) == 0
        winners = 'infection'
    countUnits = 0
    for squadNo in system[winners]:
        countUnits += system[winners][squadNo].getNumUnits()
    return ( winners, countUnits )

def findAddedPowerForImmuneWin( input ):
    highestKnownInfectionWin = 0
    lowestFoundImmuneWin = None
    testImmuneWin = 50
    while not lowestFoundImmuneWin:
        system = parseInput( input, testImmuneWin )
        runSimulation( system )
        (winners,countUnits) = countNumWinningUnits( system )
        print( 'boost:', testImmuneWin, 'winners:', winners, countUnits )
        if winners == 'infection':
            highestKnownInfectionWin = testImmuneWin
            testImmuneWin *= 2
        else:
            assert winners == 'immune'
            lowestFoundImmuneWin = testImmuneWin
    print( 'binary find between:', highestKnownInfectionWin, lowestFoundImmuneWin )
    while highestKnownInfectionWin < lowestFoundImmuneWin - 1:
        testImmuneWin = int((highestKnownInfectionWin + lowestFoundImmuneWin) / 2)
        system = parseInput( input, testImmuneWin )
        runSimulation( system )
        (winners,countUnits) = countNumWinningUnits( system )
        if winners == 'infection' or winners == 'draw':
            highestKnownInfectionWin = testImmuneWin
        else:
            assert winners == 'immune'
            lowestFoundImmuneWin = testImmuneWin
        print( highestKnownInfectionWin, lowestFoundImmuneWin, 'boost:', testImmuneWin, 'winners:', winners, countUnits )
    return lowestFoundImmuneWin
    
input = readInput()
#lowestFoundImmuneWin = findAddedPowerForImmuneWin( input )
lowestFoundImmuneWin = 29
system = parseInput( input, lowestFoundImmuneWin )
system['debug'] = print
runSimulation( system )
print( countNumWinningUnits( system ) )
