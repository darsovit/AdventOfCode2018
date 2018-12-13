#!python
'''
Advent of Code 2018, Day 12, 2nd Part
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

def convertPots( rule ):
    value = 0
    bitCount = 0
    for i in list(rule):
        if i == '#':
            value = (1<<bitCount) + value
        bitCount += 1
            
    return value
    
def convertStateToMachineAndValue( state ):
    machine = [ None ] * 32
    for rule in state['rules'].keys():
        machine[convertPots(rule)] = convertPots( state['rules'][rule] )
    print( 'machine', machine )
    value = convertPots( state['pots'] )
    return ( machine, ( value, 0 ) )

def runMachine( machine, valueAndFirstPotBit ):
    (value, firstPotBit) = valueAndFirstPotBit

    initialFilter = [ 0x1, 0x3, 0x7, 0xf ]
    initialLeftShifts = [ 4, 3, 2, 1 ]
    newFirstPotBit = firstPotBit - 2
    newValue = 0
    bitCount = 0
    for i in range(4):
        index = (value & initialFilter[i]) << initialLeftShifts[i]
        bit = machine[index]
        #print( bitCount, index, bit, firstPotBit - 2 + bitCount )
        newValue = (bit << bitCount) + newValue
        bitCount += 1
            
    while value > 0:
        index = (value & 0x1f)
        bit = machine[index]
        #print( bitCount, index, bit, firstPotBit - 2 + bitCount )
        newValue = (bit << bitCount) + newValue
        bitCount += 1
        value >>= 1
    #print( 'newValue', newValue )
    while ( (newValue & 0x1) == 0 ):
        #print( 'reduction', newValue )
        newFirstPotBit += 1
        newValue >>= 1
        
    return ( newValue, newFirstPotBit )

def debugPrint( count, valueAndFirstPotBit ):
    (value,firstPotBit) = valueAndFirstPotBit
    printableVal = ''
    while value > 0:
        lowestBit = (value&1)
        if lowestBit == 1:
            printableVal += '#'
        else:
            assert(lowestBit == 0)
            printableVal += '.'
        value >>= 1    
        
    print( count, printableVal, firstPotBit )

def calculateFilledPotValue( repeatingValue, totalNumToComplete ):
    (value,firstPotBit,iterationsComplete,incrementPerIteration) = repeatingValue
    iterationsToGo = totalNumToComplete - (iterationsComplete+1)
    firstPotBit += ( iterationsToGo * incrementPerIteration )
    
    potSum = 0
    while ( value > 0 ):
        lowestBit = (value&1)
        potSum += ( lowestBit * firstPotBit )
        firstPotBit += 1
        value >>= 1
    return potSum
    
( machine, value ) = convertStateToMachineAndValue( readInputFile() )
numIterations = 50000000000
repeatingValue = None
for i in range(numIterations):
    #debugPrint(i, value)
    newValue = runMachine( machine, value )
    if ( newValue[0] == value[0] ):
        repeatingValue = ( newValue[0], newValue[1], i, newValue[1]-value[1] )
        break
    else:
        value = newValue

print( calculateFilledPotValue ( repeatingValue, numIterations ) )
