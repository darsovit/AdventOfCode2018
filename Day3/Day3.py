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
    
elfPlans = loadInput()