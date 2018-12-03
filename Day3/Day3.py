#!python
'''
Advent of Code 2018, Day 3, First problem
Overlapping Elf plans
'''

def loadInput():
    claims = dict()
    with open('input.txt') as f:
        for line in f:
           (claim, at, pos, size) = line.split()
           claim = int(claim[1:])
           (left,top) = map(int, pos[:-1].split(','))
           (width,height) = map(int, size.split('x'))
           claims[claim] = {'left': left, 'top': top, 'width': width, 'height': height}
    return claims

def evaluatePlans( plans ):
    fabric = []
    for y in range(0,1000):
        fabric = fabric + [bytearray(1000)]
    overlapSquareInches = 0
    for plan in plans.keys():
        for y in range(plans[plan]['top'], plans[plan]['top']+plans[plan]['height']):
            for x in range(plans[plan]['left'], plans[plan]['left']+plans[plan]['width']):
                if (fabric[y][x] == 0):
                    fabric[y][x] = 1
                elif (fabric[y][x] == 1):
                    fabric[y][x] = 2
                    overlapSquareInches += 1
    return overlapSquareInches

elfPlans = loadInput()
print( int(evaluatePlans(elfPlans)) )