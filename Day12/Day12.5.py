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
    newValue = None
    initialFilter = [ 0x1, 0x3, 0x7, 0xf ]
    initialLeftShifts = [ 4, 3, 2, 1 ]
    newFirstPotBit = None
    bitCount = 0
    for i in range(2):
        bit = machine[( value & initialFilter[i] ) << initialLeftShifts[i]]
        if not newValue:
            if bit == 1:
                newValue = bit
                newFirstPotBit = firstPotBit - 2 + i
                bitCount = 1
        else:
            newValue = bit << bitCount + newValue
            bitCount += 1
    if not newValue:
        newValue = 0
        newFirstPotBit = firstPotBit

    for i in range(2,4):
        bit = machine[( value & initialFilter[i] ) << initialLeftShifts[i]]
        newValue = (bit << bitCount) + newValue
        bitCount += 1
            
    while value > 0:
        nextBit = machine[( value & 0x10 )]
        newValue = (bit << bitCount) + newValue
        bitCount += 1
        value >>= 1
        
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


( machine, value ) = convertStateToMachineAndValue( getTestState() )

for i in range(20):
    debugPrint(i, value)
    value = runMachine( machine, value )

debugPrint(20, value)
print( value )