#!python
'''
Advent of Code 2018, Day 10, Part 1
https://adventofcode.com/2018/day/10
'''
import re

def readInputLines():
    lines = [
        'position=< 9,  1> velocity=< 0,  2>',
        'position=< 7,  0> velocity=<-1,  0>',
        'position=< 3, -2> velocity=<-1,  1>',
        'position=< 6, 10> velocity=<-2, -1>',
        'position=< 2, -4> velocity=< 2,  2>',
        'position=<-6, 10> velocity=< 2, -2>',
        'position=< 1,  8> velocity=< 1, -1>',
        'position=< 1,  7> velocity=< 1,  0>',
        'position=<-3, 11> velocity=< 1, -2>',
        'position=< 7,  6> velocity=<-1, -1>',
        'position=<-2,  3> velocity=< 1,  0>',
        'position=<-4,  3> velocity=< 2,  0>',
        'position=<10, -3> velocity=<-1,  1>',
        'position=< 5, 11> velocity=< 1, -2>',
        'position=< 4,  7> velocity=< 0, -1>',
        'position=< 8, -2> velocity=< 0,  1>',
        'position=<15,  0> velocity=<-2,  0>',
        'position=< 1,  6> velocity=< 1,  0>',
        'position=< 8,  9> velocity=< 0, -1>',
        'position=< 3,  3> velocity=<-1,  1>',
        'position=< 0,  5> velocity=< 0, -1>',
        'position=<-2,  2> velocity=< 2,  0>',
        'position=< 5, -2> velocity=< 1,  2>',
        'position=< 1,  4> velocity=< 2,  1>',
        'position=<-2,  7> velocity=< 2, -2>',
        'position=< 3,  6> velocity=<-1, -1>',
        'position=< 5,  0> velocity=< 1,  0>',
        'position=<-6,  0> velocity=< 2,  0>',
        'position=< 5,  9> velocity=< 1, -2>',
        'position=<14,  7> velocity=<-2,  0>',
        'position=<-3,  6> velocity=< 2, -1>'
    ]
    #return lines
    with open('input.txt') as f:
        return list( map(str.rstrip, f.readlines() ) )

def parseStars( lines ):
    stars = []
    for line in lines:
        star = {}
        starData = re.split('[=<>, ]+', line)
        star['initial'] = (int(starData[1]), int(starData[2]))
        star['velocity'] = (int(starData[4]), int(starData[5]))
        stars += [ star ]
    return stars


def starPositions( stars, numSeconds ):
    field = {}
    for star in stars:
        posY = star['initial'][1] + star['velocity'][1]*numSeconds
        posX = star['initial'][0] + star['velocity'][0]*numSeconds
        if posY not in field:
            field[posY] = set()            
        field[posY].add( posX )
    return field
    

stars = parseStars( readInputLines() )

numSeconds = 0
readable   = False
lastField = {}
lastFieldRasterLines = None

while not readable:
    numSeconds += 1
    if ( numSeconds % 100 == 0 ):
        print( 'Seconds calculated: ', numSeconds, ', raster lines: ', lastFieldRasterLines )
    field = starPositions( stars, numSeconds )

    fieldRasterLines = len(field.keys())
    if lastFieldRasterLines and ( lastFieldRasterLines < fieldRasterLines ):
        readable = True
    elif not lastFieldRasterLines or ( fieldRasterLines < lastFieldRasterLines ):
        lastField = field
        lastFieldRasterLines = fieldRasterLines
    else:
        lastField = field  # same number of raster lines


print( lastFieldRasterLines, numSeconds-1 )
for line in lastField:
    print(line)
    points = list(lastField[line])
    points.sort()
    print( points )
