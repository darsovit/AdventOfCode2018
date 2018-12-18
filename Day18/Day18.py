#!python
'''
Advent of Code 2018, Day 18
https://adventofcode.com/2018/day/18
'''

def getInputLines():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))
        
def getSampleLines():
    return [
        '.#.#...|#.',
        '.....#|##|',
        '.|..|...#.',
        '..|#.....#',
        '#.#|||#|#|',
        '...#.||...',
        '.|....|...',
        '||...#|.#|',
        '|.||||..|.',
        '...#.|..|.'
    ]

def countInAdjacents( letter, adjacents ):
    count = 0
    for adjacent in adjacents:
        if adjacent == letter:
            count += 1
    return count

def calculateNewField( positionChar, adjacents ):
    newChar = positionChar
    if positionChar == '.':
        if 3 <= countInAdjacents( '|', adjacents ):
            newChar = '|'
    elif positionChar == '|':
        if 3 <= countInAdjacents( '#', adjacents ):
            newChar = '#'
    elif positionChar == '#':
        if 1 <= countInAdjacents( '#', adjacents ) and 1 <= countInAdjacents('|', adjacents):
            newChar = '#'
        else:
            newChar = '.'
    return newChar

def transformField( lines ):
    newLines = []
    newLines.append('')
    newLines[0] = calculateNewField(lines[0][0], [ lines[0][1] ] + list(lines[1][0:2]) )
    for x in range(1,len(lines[0])-1):
        newLines[0] += calculateNewField(lines[0][x], [ lines[0][x-1], lines[0][x+1] ] + list( lines[1][x-1:x+2] ) )
    for x in range(len(lines[0])-1, len(lines[0])):
        newLines[0] += calculateNewField(lines[0][x], [ lines[0][x-1] ] + list( lines[1][x-1:] ) )
            
    for y in range(1,len(lines)-1):
        newLines.append('')
        newLines[y] = calculateNewField(lines[y][0], list(lines[y-1][0:2]) + [ lines[y][1] ] + list(lines[y+1][0:2] ) )
        for x in range(1, len(lines[y])-1):
            newLines[y] += calculateNewField(lines[y][x], list(lines[y-1][x-1:x+2]) + [ lines[y][x-1], lines[y][x+1] ] + list(lines[y+1][x-1:x+2]) )
        for x in range(len(lines[y])-1,len(lines[y])):
            newLines[y] += calculateNewField(lines[y][x], list(lines[y-1][x-1:]) + [ lines[y][x-1] ] + list(lines[y+1][x-1:]) )
    newLines.append('')
    for y in range(len(lines)-1,len(lines)):
        newLines[y] = calculateNewField( lines[y][0], list(lines[y-1][0:2]) + [ lines[y][1] ] )
        for x in range(1, len(lines[y])-1):
            newLines[y] += calculateNewField(lines[y][x], list(lines[y-1][x-1:x+2]) + [ lines[y][x-1], lines[y][x+1] ] )
        for x in range(len(lines[y])-1,len(lines[y])):
            newLines[y] += calculateNewField(lines[y][x], list(lines[y-1][x-1:]) + [ lines[y][x-1] ] )
    return newLines
    
def printField( lines ):
    for line in lines:
        print( line )

def transformXMins( lines, times ):
    newField = lines
    for time in range(times):
        newField = transformField( newField )
    return newField

def valueOfField( lines ):
    countLumberYards = 0
    countWooded      = 0
    for line in lines:
        countLumberYards += countInAdjacents( '#', list(line) )
        countWooded      += countInAdjacents( '|', list(line) )
    return ( countLumberYards, countWooded, countLumberYards * countWooded )

tenMinuteField = transformXMins(getInputLines(), 10)
printField( tenMinuteField )
print( valueOfField( tenMinuteField ) )