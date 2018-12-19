#!python
'''
Advent of Code 2018, Day 16
https://adventofcode.com/2018/day/16
'''

def readSamples():
    with open('input.txt') as f:
        state = 0
        beginVals = []
        opInput   = []
        samples = []
        for line in list(map(str.rstrip, f.readlines())):
            if state == 0 and len(line) > 6 and "Before" == line[0:6]:
                state = 1
                beginVals = line[9:-1].split(', ')
            elif state == 1:
                opInput = line.split(' ')
                state = 2
            elif state == 2 and len(line) > 5 and 'After' == line[0:5]:
                afterVals = line[9:-1].split(', ')
                samples += [(beginVals,afterVals,opInput)]
        return samples        
            
print( readSamples() )