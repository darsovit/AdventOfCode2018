#!python
'''
Advent of Code 2018, Day 17
https://adventofcode.com/2018/day/17
'''
from collections import deque

def sampleInput():
    return [
        "x=495, y=2..7",
        "y=7, x=495..501",
        "x=501, y=3..7",
        "x=498, y=2..4",
        "x=506, y=1..2",
        "x=498, y=10..13",
        "x=504, y=10..13",
        "y=13, x=498..504"
    ]
    
def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def getValue( equalVal ):
    return equalVal.split('=')[1]

def getRange( coordRangeVal ):
    rangeVal = getValue( coordRangeVal )
    (start,end) = list( map( int, rangeVal.split('..') ) )
    return iter( range(start, end+1) )
    
def buildField( lines ):
    field = {}
    field['clay'] = set()
    field['deepest'] = None
    field['minY']    = None
    field['leftest'] = 500
    field['rightest'] = 500
    
    for line in lines:
        coords = line.split(', ')
        if line[0] == 'x':
            x = int( getValue(coords[0]) )
            if x > field['rightest']:
                field['rightest'] = x
            elif x < field['leftest']:
                field['leftest'] = x
            for y in getRange(coords[1]):
                field['clay'].add( (x, y) )
                if not field['minY']:
                    field['minY'] = y
                    field['deepest'] = y
                if y < field['minY']:
                    field['minY'] = y
                elif y > field['deepest']:
                    field['deepest'] = y

        elif line[0] == 'y':
            y = int( getValue( coords[0]) )
            if not field['minY']:
                field['minY'] = y
                field['deepest'] = y
            if y > field['deepest']:
                field['deepest'] = y
            for x in getRange(coords[1]):
                field['clay'].add( (x, y ) )                
                if x > field['rightest']:
                    field['rightest'] = x
                elif x < field['leftest']:
                    field['leftest'] = x
    return field

def wallToLeft( field, pos ):
    (x,y) = pos
    return (x-1,y) in field['clay']

def wallToRight( field, pos ):
    (x, y) = pos
    return (x+1,y) in field['clay']

def solidUnderLeft( field, pos ):
    (x, y) = pos
    testPos = (x-1,y+1)
    return testPos in field['clay'] or testPos in field['water'] and '~' == field['water'][testPos]

def solidUnderRight( field, pos ):
    (x, y) = pos
    testPos = (x+1, y+1)
    return testPos in field['clay'] or testPos in field['water'] and '~' == field['water'][testPos]
    
def testInBasin( field, pos ):
    (x,y) = pos
    # test left
    leftX = x
    while not wallToLeft( field, (leftX,y) ) and solidUnderLeft( field, (leftX, y) ):
        leftX -= 1
        field['water'][(leftX,y)] = '|'
    rightX = x
    while not wallToRight( field, (rightX,y) ) and solidUnderRight( field, (rightX, y) ):
        rightX += 1
        field['water'][(rightX,y)] = '|'
    if wallToLeft( field, (leftX,y) ) and wallToRight( field, (rightX, y) ):
        return ( True, (leftX,y), (rightX,y) )
    if wallToLeft( field, (leftX,y) ):
        field['water'][(rightX+1,y)] = '|'
        return ( False, None, (rightX+1,y) )
    elif wallToRight( field, (rightX,y) ):
        field['water'][(leftX-1,y)] = '|'
        return ( False, (leftX-1,y), None )
    else:
        field['water'][(leftX-1,y)] = '|'
        field['water'][(rightX+1,y)] = '|'
        return ( False, (leftX-1,y), (rightX+1, y) )

def fillBasin( field, left, right ):
    (leftX,y) = left
    (rightX,y) = right
    for i in range(leftX,rightX+1):
        field['water'][(i,y)] = '~'
    
def fillWater( field ):
    waterPos = (500,0)
    field['downstream'] = deque()
    field['downstream'].appendleft(waterPos)
    field['water'] = {}
    field['water'][waterPos] = '|'
    while len(field['downstream']) > 0:
        (x,y) = field['downstream'].popleft()
        while (x,y+1) not in field['clay'] and (x,y+1) not in field['water'] and y+1 <= field['deepest']:
            y += 1
            field['water'][(x,y)] = '|'

        if not y == field['deepest']:
            # We've hit clay or our water stream cannot flow down any longer
            (inBasin, left, right) = testInBasin( field, (x,y) )
            if inBasin:
                fillBasin( field, left, right )
                field['downstream'].appendleft( (x,y-1) )
            else:
                if left:
                    field['downstream'].appendleft( left )
                if right:
                    field['downstream'].appendleft( right )

def debugPrint( field ):
    for y in range(0,field['deepest']+1):
        for x in range(field['leftest']-2,field['rightest']+3):
            if (x,y) in field['clay']:
                print('#',end='')
            elif (x,y) in field['water']:
                print(field['water'][(x,y)], end='')
            else:
                print('.', end='')
        print()
def countWaterTiles( field ):
    count = 0
    for waterTile in field['water']:
        (x,y) = waterTile
        if y >= field['minY'] and y <= field['deepest']:
            count += 1
    return count
        
field = buildField( readInput() )
fillWater( field )
debugPrint( field )
print( countWaterTiles( field ) )