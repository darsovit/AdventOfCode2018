#!python
'''
Advent of Code, Day 2, 2nd Puzzle
Find the edit distance of 1 strings
'''

def loadLines():
    lines = []
    with open('input.txt') as f:
        for line in f:
            lines = lines + [ line.rstrip() ]
    return lines

def evaluateLines(lines):
    for i in range(0,len(lines)-1):
        for j in range(i+1,len(lines)):
            done = compareLines(lines[i], lines[j])
            if done:
                return (lines[i], lines[j])
    return ("", "")

def compareLines(line1, line2):
    diffCount = 0
    for i in range(0,len(line1)):
        if line1[i] != line2[i]:
            diffCount += 1
            if diffCount > 1:
                return False
    return diffCount == 1

def combineLines(line1,line2):
    sameletters = []
    for i in range(0,len(line1)):
        if line1[i] == line2[i]:
            sameletters += [line1[i]]
    return ''.join(sameletters)

lines = loadLines()
(line1, line2) = evaluateLines(lines)
print(combineLines(line1,line2))

