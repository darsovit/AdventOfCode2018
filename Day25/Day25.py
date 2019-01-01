#! python
'''
Advent of Code 2018, Day 25
https://adventofcode.com/2018/day/25
'''

def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )
        
def tests():
    return [
        ( [ '0,0,0,0',
            '3,0,0,0',
            '0,3,0,0',
            '0,0,3,0',
            '0,0,0,3',
            '0,0,0,6',
            '9,0,0,0',
           '12,0,0,0' ], 2 ),
        ( [ '0,0,0,0',
            '3,0,0,0',
            '0,3,0,0',
            '0,0,3,0',
            '0,0,0,3',
            '0,0,0,6',
            '9,0,0,0',
           '12,0,0,0',
            '6,0,0,0'], 1 ),
        ( [ '-1,2,2,0',
            '0,0,2,-2',
            '-1,2,0,0',
            '-2,-2,-2,2',
            '3,0,2,-1',
            '-1,3,2,2',
            '-1,0,-1,0',
            '0,2,1,-2',
            '3,0,0,0' ], 4 ),
        ( [ '1,-1,0,1',
            '2,0,-1,0',
            '3,2,-1,0',
            '0,0,3,1',
            '0,0,-1,-1',
            '2,3,-2,0',
            '-2,2,0,0',
            '2,-2,0,-1',
            '1,-1,0,-1',
            '3,2,0,2' ], 3 ),
        ( [ '1,-1,-1,-2',
            '-2,-2,0,1',
            '0,2,1,3',
            '-2,3,-2,1',
            '0,2,3,-2',
            '-1,-1,1,-2',
            '0,-2,-1,0',
            '-2,2,3,-1',
            '1,2,2,0',
            '-1,-2,0,-2' ], 8 )
    ]
    
def parseToPoints( lines ):
    points = []
    for line in lines:
        points += [ tuple( map( int, line.split(',') ) ) ]
    return points

def manhattanDistance( start, end ):
    return abs( start[0] - end[0] ) + abs( start[1] - end[1] ) + abs( start[2] - end[2] ) + abs( start[3] - end[3] )

def buildConstellations( points ):
    constellationGraph = {}
    constellationMap   = {}
    constellationNum   = 1
    
    for point in points:
        addedToGraph = None
        for item in constellationGraph:
            if manhattanDistance( point, item ) <= 3:
                if not addedToGraph:
                    addedToGraph = constellationGraph[item]
                    constellationMap[addedToGraph].add( point )
                elif addedToGraph != constellationGraph[item]:
                    addlConstellation = constellationGraph[item]
                    for movedPoint in constellationMap[addlConstellation]:
                        constellationMap[addedToGraph].add( movedPoint )
                        assert movedPoint in constellationGraph
                        constellationGraph[movedPoint] = addedToGraph
                    del constellationMap[addlConstellation]
                else:
                    assert addedToGraph == constellationGraph[item]
        if not addedToGraph:
            constellationGraph[point] = constellationNum
            constellationMap[constellationNum] = set()
            constellationMap[constellationNum].add( point )
            constellationNum += 1
        else:
            constellationGraph[point] = addedToGraph
    return constellationMap

for (inputPts,expected) in tests():
    constellations = buildConstellations( parseToPoints( inputPts ) )
    print( constellations, expected )
    assert expected == len( constellations ), (inputPts, expected)

inputConstellations = buildConstellations( parseToPoints( readInput() ) )
print (inputConstellations, len(inputConstellations) )
