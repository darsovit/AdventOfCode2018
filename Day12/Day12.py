#!python
'''
Advent of Code 2018, Day 12
https://adventofcode.com/2018/day/12
'''

def readInputFile():
    state = {}
    state['rules'] = {}
    with open('input.txt') as f:
        for line in list( map( str.rstrip, f.readlines() ) ):
            if len(line) == 0:
                continue
            input = line.split(' ')
            if len(input) == 3 and 'initial' == input[0]:
                state['startPos'] = 0
                state['pots']     = input[2]
            elif len(input) == 3 and '=>' == input[1]:
                state['rules'][input[0]] = input[2]
    return state

def getTestState():
    state = {}
    state['rules'] = {}
    state['startPos'] = 0
    state['pots']  = '#..#.#..##......###...###'
    state['rules']['.....'] = '.'
    state['rules']['....#'] = '.'
    state['rules']['...#.'] = '.'
    state['rules']['...##'] = '#'
    state['rules']['..#..'] = '#'
    state['rules']['..#.#'] = '.'
    state['rules']['..##.'] = '.'
    state['rules']['..###'] = '.'
    state['rules']['.#...'] = '#'
    state['rules']['.#..#'] = '.'
    state['rules']['.#.#.'] = '#'
    state['rules']['.#.##'] = '#'
    state['rules']['.##..'] = '#'
    state['rules']['.##.#'] = '.'
    state['rules']['.###.'] = '.'
    state['rules']['.####'] = '#'
    state['rules']['#....'] = '.'
    state['rules']['#...#'] = '.'
    state['rules']['#..#.'] = '.'
    state['rules']['#..##'] = '.'
    state['rules']['#.#..'] = '.'
    state['rules']['#.#.#'] = '#'
    state['rules']['#.##.'] = '.'
    state['rules']['#.###'] = '#'
    state['rules']['##...'] = '.'
    state['rules']['##..#'] = '.'
    state['rules']['##.#.'] = '#'
    state['rules']['##.##'] = '#'
    state['rules']['###..'] = '#'
    state['rules']['###.#'] = '#'
    state['rules']['####.'] = '#'
    state['rules']['#####'] = '.'
    return state

def calculateNextState( state ):
    startOfCalc = state['startPos'] - 2
    endOfCalc   = state['startPos'] + len(state['pots']) + 2
    newPots     = []
    for i in range( startOfCalc, state['startPos'] + 2 ):
        leftMostCalculationPos = i - 2
        numEmptiesBefore = state['startPos'] - leftMostCalculationPos
        numPots          = 5 - numEmptiesBefore
        myPots = '.' * numEmptiesBefore + state['pots'][:numPots]
        newPots += [ state['rules'][myPots] ]
    for i in range( state['startPos'] + 2, state['startPos']+len(state['pots'])-2 ):
        rangeOfPotStart = i - state['startPos']
        myPots = state['pots'][rangeOfPotStart-2:rangeOfPotStart+3]
        newPots += [ state['rules'][myPots] ]
    for i in range( state['startPos'] + len( state['pots']) - 2, state['startPos']+len(state['pots'])+2 ):
        rightMostCalculationPos = i + 2
        numEmptiesAfter = rightMostCalculationPos - (state['startPos']+len(state['pots']) - 1)
        numPots = 5 - numEmptiesAfter
        myPots = state['pots'][-numPots:] + '.' * numEmptiesAfter
        newPots += [ state['rules'][myPots] ]
    firstPlant = None
    lastPlant  = None
    for i in range(len(newPots)):
        if newPots[i] == '#':
            firstPlant = i
            break
    for i in range(len(newPots)-1,-1,-1):
        if newPots[i] == '#':
            lastPlant = i
            break
    if lastPlant < ( len(newPots) - 1):
        newPots = newPots[:lastPlant+1]
    if firstPlant > 0:
        newPots = newPots[firstPlant:]
        startOfCalc += firstPlant
    state['startPos'] = startOfCalc
    state['pots'] = ''.join( newPots )
    return state

def calculateValueOfPots( pots, startPos ):
    value = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            value += ( startPos + i )
    return value



#state = getTestState()
state = readInputFile()

for i in range(20):
    state = calculateNextState( state )

print( calculateValueOfPots( state['pots'], state['startPos'] ) )
