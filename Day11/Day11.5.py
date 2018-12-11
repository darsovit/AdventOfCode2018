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

def calculateField( serial,size ):
    field = {}
    field['size'] = size
    powerLevel = 0
    for x in range(1,size+1):
        for y in range(1,size+1):
            field[(x,y)] = calculatePowerLevel( serial, x, y )
    return field

def printField( field ):
    size = field['size']
    for x in range( 1, size+1 ):
        linevalues = []
        for y in range( 1, size+1 ):
            linevalues += [ '{0:>2}'.format(field[(x,y)]) ]
        print( ' '.join( linevalues ) )

def addToSquare( field, currentSquareValue, x, y, squareSize ):
    for deltaY in range(squareSize-1):
        currentSquareValue += field[(x+squareSize-1,y+deltaY)]
    for deltaX in range(squareSize-1):
        currentSquareValue += field[(x+deltaX, y+squareSize-1)]
    currentSquareValue += field[(x+squareSize-1, y+squareSize-1)]
    return currentSquareValue

def calculatePossibleSquares( field ):
    #print(field)
    largestSquareValue = field[(1,1)]
    largestSquarePos   = (1,1,1)
    fieldSize = field['size']
    for x in range( 1, fieldSize+1 ):
        for y in range( 1, fieldSize+1 ):
            if x == y:
                print("Current: ", x, y )
            maxX = fieldSize + 1 - x
            maxY = fieldSize + 1 - y
            maxSquare = min(maxX,maxY)
            #print( 'MaxSquare', (x,y), maxSquare )
            currentSquareSize = 1
            currentSquareValue = field[(x,y)]
            if ( currentSquareValue > largestSquareValue ):
                largestSquareValue = currentSquareValue
                largestSquarePos   = (x,y,1)
            #print( currentSquareValue, (x,y,currentSquareSize) )
            for squareSize in range(2,maxSquare+1):
                currentSquareValue = addToSquare( field, currentSquareValue, x, y, squareSize )
                currentSquareSize = squareSize
                #print( 'currentSquareValue:', (x,y,squareSize), currentSquareValue )
                if ( currentSquareValue > largestSquareValue ):
                    largestSquareValue = currentSquareValue
                    largestSquarePos   = (x,y,currentSquareSize)
    return ( largestSquareValue, largestSquarePos )

field = calculateField( 5034, 300 )
print( calculatePossibleSquares( field ) )