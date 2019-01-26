#! python

'''
Advent of Code 2018, Day 17
Attempt to solve via TDD
'''

def buildRasterLines(clayScanLines):
    rasterLines = dict()
    for line in clayScanLines:
        (single,multi) = line.split(',')
        (singleCoord,value) = single.split('=')
        (multiCoord,multiValues) = multi.split('=')
        (minMultiVal,maxMultiVal) = list( map( int, multiValues.split('..') ) )
        if singleCoord == 'x':
            for i in range(minMultiVal,maxMultiVal+1):
                if i not in rasterLines:
                    rasterLines[i] = set()
                rasterLines[i].add( int(value) )
        else:
            assert singleCoord == 'y'
            if int(value) not in rasterLines:
                rasterLines[int(value)] = set()
            for i in range(minMultiVal,maxMultiVal+1):
                rasterLines[int(value)].add( i )
    return rasterLines
    
def countFlowThroughRasterLines( rasterLines ):
    if rasterLines:
        return max( rasterLines )+1 - min( rasterLines )
    else:
        return 0

def calcFlow(clayScanLines):
    scanLines = buildRasterLines( clayScanLines )
    return countFlowThroughRasterLines( scanLines )

def test1():
    # Empty set
    assert 0 == calcFlow([])

def test2():
    # (0)     x
    # (1)   ##|
    # (2)   ..|
    assert 1 == calcFlow(['y=1,x=498..499'])

def test3():
    # (0)    x
    # (1)   #|
    # (2)   #|
    # (3)   .|
    assert 2 == calcFlow(['x=499,y=1..2'])
    
def test4():
    # (0)      x
    # (1)     .|
    # (2..99) .|
    # (100)   #|
    # (101)   #|
    # (102)   .|
    assert 2 == calcFlow(['x=499,y=100..101'])

def test5():
    # (0)      x
    # (1)    ##|    1st input
    # (2)    ..|
    # (3)    ..|
    # (4)    ##|    2nd input
    # (5)    ..|
    assert 4 == calcFlow(['y=1,x=498..499','y=4,x=498..499']), calcFlow(['y=1,x=498..499','y=4,x=498..499'])

def test6():
    # (0)      x
    # (1)    ##|    2nd input
    # (2)    ..|
    # (3)    ..|
    # (4)    ##|    1st input
    # (5)    ..|
    assert 4 == calcFlow(['y=4,x=498..499','y=1,x=498..499']), calcFlow(['y=4,x=498..499','y=1,x=498..499'])
    
def test7():
    # (0)      x
    # (1)    ##|
    # (2)    ..|
    # (3)    ..|#
    # (4)    ..|#
    # (5)    ..|#
    assert 5 == calcFlow(['y=1,x=498..499','x=501,y=3..5'])

def test8():
    # (0)     x
    # (1)    .|..
    # (2)    ||##
    # (3)    |##.
    # (4)    |...
    assert 3 == calcFlow(['y=2,x=501..502','y=3,x=500..501']), calcFlow(['y=2,x=501..502','y=3,x=500..501'])

def test9():
    # (0)    x
    # (1)   .|.
    # (2)   |||
    # (3)   |#|
    # (4)   |#|
    # (5)   |.|
    assert 4 == calcFlow(['x=500,y=3..4']), calcFlow(['x=500,y=3..4'])

test1()
test2()
test3()
test4()
test5()
test6()
test7()
#test8()
test9()
