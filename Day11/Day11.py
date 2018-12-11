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

def calculateGridAt( serial, field, x, y, debug ):
    powerLevel = 0
    for deltaX in range(0,3):
        for deltaY in range(0, 3):
            newX = x+deltaX
            newY = y+deltaY
            if (newX,newY) not in field:
                cellLevel = calculatePowerLevel( serial, newX, newY )
                if debug:
                    print( (newX,newY) , 'not in field, calculated cellLevel = ', cellLevel )
                field[(newX,newY)] = cellLevel
                powerLevel += cellLevel
            else:
                if debug:
                    print( (newX,newY) , 'found in field, using powerLevel = ', field[(newX,newY)] )
                powerLevel += field[(newX,newY)]
    if ( debug ):
        print( 'powerLevel calculated for 3x3 grid at:', (x,y), powerLevel )
    return powerLevel

def findLargest3x3in300x300( serial ):
    maxPossible = 4*9
    fieldOf3x3 = {}
    field = {}
    largestPos = None
    largestVal = None
    
    for x in range(1,299):
        for y in range(1,299):
            if ( x == 33 ) and ( y == 45 ):
                powerLevel = calculateGridAt( serial, field, x, y, False )
            else:
                powerLevel = calculateGridAt( serial, field, x, y, False )
            if ( x == 33 ) and ( y == 45 ):
                print( powerLevel )
            fieldOf3x3[(x,y)] = powerLevel
            if not largestPos or powerLevel > largestVal:
                largestVal = powerLevel
                largestPos = (x,y)
                if largestVal == maxPossible:
                    return ( largestVal, (x,y) )

    return ( largestVal, largestPos )
    
print( findLargest3x3in300x300( 18 ) )
print( findLargest3x3in300x300( 42 ) )
print( findLargest3x3in300x300( 5034 ) )