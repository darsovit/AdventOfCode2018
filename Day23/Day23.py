#!python
'''
Advent of Code 2018, Day 23
https://adventofcode.com/2018/day/23
'''

def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )
        
def sampleInput():
    return [
        'pos=<0,0,0>, r=4',
        'pos=<1,0,0>, r=1',
        'pos=<4,0,0>, r=3',
        'pos=<0,2,0>, r=1',
        'pos=<0,5,0>, r=3',
        'pos=<0,0,3>, r=1',
        'pos=<1,1,1>, r=1',
        'pos=<1,1,2>, r=1',
        'pos=<1,3,1>, r=1'
    ]
    
def parseInput( input ):
    nanobots = []
    largestRange = 0
    largestRangeIndex = 0
    count = 0
    for line in input:
        ( posStr, rangeStr ) = line.split(', ')
        range = int(rangeStr[2:])
        if range > largestRange:
            largestRange = range
            largestRangeIndex = count
        (x,y,z) = list( map( int, posStr[5:-1].split(',') ) )
        nanobots.append( (x,y,z,range) )
        count += 1
    return ( nanobots, largestRangeIndex )

def distanceBetweenNanobots( nanobot1, nanobot2 ):
    return abs( nanobot1[0] - nanobot2[0] ) + abs( nanobot1[1] - nanobot2[1] ) + abs( nanobot1[2] - nanobot2[2] )

def countNanobotsInRange( nanobots, nanobot ):
    count = 0
    for i in range( len(nanobots) ):
        if distanceBetweenNanobots( nanobots[i], nanobot ) <= nanobot[3]:
            count += 1
    return count

(nanobots, largestRangeIndex) = parseInput( readInput() )
print( countNanobotsInRange( nanobots, nanobots[170] ) )