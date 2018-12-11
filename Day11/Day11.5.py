#!python
'''
Advent of Code 2018, Day 11, Part 1
https://adventofcode.com/2018/day/11
'''

def calculatePowerLevel( serial, x, y ):
    rackId = x + 10
    
    powerLevel = int( ( ( ( rackId * y + serial ) * rackId ) % 1000 ) / 100 ) - 5
    assert( powerLevel <= 4 and powerLevel >= -5 )
    return powerLevel

#print( calculatePowerLevel( 8, 3, 5 ) )
#print( calculatePowerLevel( 57, 122, 79 ) )
#print( calculatePowerLevel( 39, 217, 196 ) )
#print( calculatePowerLevel( 71, 101, 153 ) )

#print( calculatePowerLevel( 18, 32, 45 ), calculatePowerLevel( 18, 33, 45 ), calculatePowerLevel( 18, 34, 45 ), calculatePowerLevel( 18, 35, 45 ), calculatePowerLevel(18, 36, 45) )
#print( calculatePowerLevel( 18, 32, 46 ), calculatePowerLevel( 18, 33, 46 ), calculatePowerLevel( 18, 34, 46 ), calculatePowerLevel( 18, 35, 46 ), calculatePowerLevel(18, 36, 46) )
#print( calculatePowerLevel( 18, 32, 47 ), calculatePowerLevel( 18, 33, 47 ), calculatePowerLevel( 18, 34, 47 ), calculatePowerLevel( 18, 35, 47 ), calculatePowerLevel(18, 36, 47) )

def calculateField( serial ):
    field = {}
    powerLevel = 0
    for x in range(1,301):
        for y in range(1,301):
            field[(x,y)] = calculatePowerLevel( serial, x, y )
    return field

def printField( field ):
    for x in range( 1, 301 ):
        linevalues = []
        for y in range( 1, 301 ):
            linevalues += [ '{0:>2}'.format(field[(x,y)]) ]
        print( ' '.join( linevalues ) )

field = calculateField( 5034 )
printField( field )