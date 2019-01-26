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
    assert 0 == calcFlow([])

def test2():
    assert 1 == calcFlow(['y=1,x=498..499'])

def test3():
    assert 2 == calcFlow(['x=499,y=1..2'])
    
def test4():
    assert 2 == calcFlow(['x=499,y=100..101'])

def test5():
    assert 4 == calcFlow(['y=1,x=498..499','y=4,x=498..499']), calcFlow(['y=1,x=498..499','y=4,x=498..499'])

def test6():
    assert 4 == calcFlow(['y=4,x=498..499','y=1,x=498..499']), calcFlow(['y=4,x=498..499','y=1,x=498..499'])
    
test1()
test2()
test3()
test4()
test5()
test6()