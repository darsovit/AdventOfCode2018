#!python
'''
Advent of Code 2018, Day 5, Part 1
https://adventofcode.com/2018/day/5
'''

def readInputPolymer():
    #return "dabAcCaCBAcCcaDA"
    with open('input.txt') as f:
        for line in f:
            return line.rstrip()

def processPolymer( polymer, index ):
    for i in range(index, len(polymer)-1):
        if polymer[i] >= 'A' and polymer[i] <= 'Z':
            if polymer[i+1] >= 'a' and polymer[i+1] <= 'z':
                if ord(polymer[i])-ord('A') == ord(polymer[i+1])-ord('a'):
                    return ( polymer[:i] + polymer[i+2:], i-1 )
        else:
            if polymer[i+1] >= 'A' and polymer[i+1] <= 'Z':
                if ord(polymer[i])-ord('a') == ord(polymer[i+1])-ord('A'):
                    return ( polymer[:i] + polymer[i+2:], i-1 )
    return ( polymer, len(polymer) )

def performReacts(polymer):
    index = 0
    while index < len(polymer):
        if ( 0 > index ):
            index = 0
        ( polymer, index ) = processPolymer( polymer, index )
    return polymer

def cleanOutLetter(letter, polymer):
    polymer = ''.join( polymer.split(letter) )
    polymer = ''.join( polymer.split(chr(ord(letter)-ord('a')+ord('A'))) )
    return polymer

inputPolymer = readInputPolymer()
shortestChain = None
shortestChar  = None
for letter in range(ord('a'),ord('z')+1):
    polymer = inputPolymer
    polymer = cleanOutLetter(chr(letter), polymer)
    polymer = performReacts(polymer)
    if not shortestChain:
        shortestChain = len(polymer)
        shortestChar  = letter
    elif (len(polymer) < shortestChain):
        shortestChain = len(polymer)
        shortestChar  = letter

print(shortestChain)
