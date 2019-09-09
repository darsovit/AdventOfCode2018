#!python
'''
Advent of Code 2018, Day 17
https://adventofcode.com/2018/day/17
'''
from collections import deque

do_debug_print = None

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
    # 499 500 501
    field['source'] = (500-field['leftest']+1, 0)
    width = field['rightest'] - field['leftest'] + 3
    field['raster'] = []
    #### DEBUG, limit to 100 depth
    #field['deepest'] = min(100,field['deepest'])
    for y in range( 0, field['deepest']+1 ):
        field['raster'].append('')
        #field['raster'][y] = bytearray(width+1)
        for x in range( 0, width + 1 ):
            if (x+field['leftest']-1, y) in field['clay']:
                field['raster'][y] += '#'
            else:
                field['raster'][y] += '.'
    return field

def getFieldElement(field, pos):
    (x,y) = pos
    return field['raster'][y][x-field['leftest']+1]

def isClay(field, pos):
    return '#' == getFieldElement(field, pos)
    
def isStillWater(field, pos):
    return '~' == getFieldElement(field, pos)

def isFlowingWater(field, pos):
    return '|' == getFieldElement(field, pos)

def isWater( field, pos ):
    element = getFieldElement(field,pos)
    return '~' == element or '|' == element

def wallToLeft( field, pos ):
    (x,y) = pos
    return isClay( field, (x-1, y) )
    
def wallToRight( field, pos ):
    (x, y) = pos
    return isClay( field, (x+1, y) )

def solidUnderLeft( field, pos ):
    (x, y) = pos
    testPos = (x-1,y+1)
    element = getFieldElement( field, testPos )
    return '#' == element or '~' == element

def solidUnderRight( field, pos ):
    (x, y) = pos
    testPos = (x+1, y+1)
    element = getFieldElement( field, testPos )
    return '#' == element or '~' == element

def fillFlowingWater( field, pos ):
    (x, y) = pos
    line = field['raster'][y]
    posToReplace = x - field['leftest'] + 1
    field['raster'][y] = line[:posToReplace] + '|' + line[posToReplace+1:]

def debugPrint( field, force_print=False ):
    if not do_debug_print and not force_print:
        return
    print('min:', field['minY'], 'deepest:', field['deepest'], 'left:', field['leftest'], 'right:', field['rightest'] )
    for y in range(0,len( field['raster'] ) ):
        for x in range( 0, len(field['raster'][y]) ):
            print(field['raster'][y][x], end='')
        print()
    print( field['downstream'] )
    input("Press enter to continue...")

def flowingWaterFromLeftToRight( field, left, right ):
    (leftX,leftY) = left
    (rightX,rightY) = right
    assert leftY == rightY
    y = leftY
    offset = -field['leftest'] + 1
    assert leftX < rightX
    rc = True
    for x in range(leftX,rightX+1):
        if not isFlowingWater( field, (x,y) ):
            debugPrint(field, True)
        assert isFlowingWater( field, (x,y) )
    return rc

def findLeftEdge( field, x, y ):
    leftX = x
    while not wallToLeft( field, (leftX,y) ) and solidUnderLeft( field, (leftX, y) ):
        leftX -= 1
    return leftX

def findRightEdge( field, x, y ):
    rightX = x
    while not wallToRight( field, (rightX,y) ) and solidUnderRight( field, (rightX, y) ):
        rightX += 1
    return rightX

def testInBasin( field, pos ):
    (x,y) = pos
    # test left
    leftX = findLeftEdge( field, x, y )
    rightX = findRightEdge( field, x, y )

    for tmpX in range(leftX,rightX+1):
        fillFlowingWater( field, (tmpX,y) )
    if wallToLeft( field, (leftX,y) ) and wallToRight( field, (rightX, y) ):
        return ( True, (leftX,y), (rightX,y) )
    if wallToLeft( field, (leftX,y) ):
        fillFlowingWater( field, (rightX+1, y) )
        return ( False, None, (rightX+1,y) )
    elif wallToRight( field, (rightX,y) ):
        fillFlowingWater( field, (leftX-1, y) )
        return ( False, (leftX-1,y), None )
    else:
        fillFlowingWater( field, (leftX-1, y) )
        fillFlowingWater( field, (rightX+1, y) )
        assert flowingWaterFromLeftToRight( field, (leftX-1,y), (rightX+1,y))
        return ( False, (leftX-1,y), (rightX+1, y) )

def fillBasin( field, left, right ):
    (leftX,y) = left
    (rightX,y) = right
    line =  field['raster'][y]
    offset = -field['leftest']+1
    countOfWater = rightX - leftX + 1
    field['raster'][y] = line[:leftX+offset] + '~'*countOfWater + line[rightX+offset+1:]
    
def fillWater( field ):
    waterPos = (500,0)
    field['downstream'] = deque()
    field['downstream'].appendleft(waterPos)
    fillFlowingWater( field, waterPos )
    debugPrint( field )
    while len(field['downstream']) > 0:
        (x,y) = field['downstream'].pop()
        
        while y+1 <= field['deepest'] and not isClay( field, (x,y+1) ) and not isWater(field, (x,y+1) ):
            y += 1
            fillFlowingWater( field, (x,y) )

        if not y == field['deepest'] and not isFlowingWater( field, (x,y+1) ):
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
        debugPrint( field )


def countWaterTiles( field ):
    retainedWater = 0
    flowingWater = 0
    for y in range(field['minY'], field['deepest']+1):
        for x in range(0, len(field['raster'][y])):
            if field['raster'][y][x] == '~':
                retainedWater += 1
            elif field['raster'][y][x] == '|':
                flowingWater += 1
    return (retainedWater, flowingWater, retainedWater+flowingWater)
    

field = buildField( readInput() )
debugPrint( field )
fillWater( field )
debugPrint( field )
print( countWaterTiles( field ) )

