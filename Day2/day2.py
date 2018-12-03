#!python
'''
Advent of Code, Day 2, first puzzle:
Checksum of boxes
https://adventofcode.com/2018/day/2
'''

count2 = 0
count3 = 0

with open('input.txt') as f:
    for line in f:
        thiscount2 = 0
        thiscount3 = 0
        line = line.rstrip()
        alphabet = {}
        print (line)
        for letter in list( line ):
            if letter in alphabet:
                alphabet[letter] = alphabet[letter]+1
                if ( alphabet[letter] == 2 ):
                    thiscount2 = thiscount2 + 1
                elif ( alphabet[letter] == 3 ):
                    thiscount2 = thiscount2 - 1
                    thiscount3 = thiscount3 + 1
                elif ( alphabet[letter] == 4 ):
                    thiscount3 = thiscount3 - 1
            else:
                alphabet[letter] = 1
        print( alphabet )
        if thiscount2 > 0:
            count2 = count2 + 1
        if thiscount3 > 0:
            count3 = count3 + 1
print ("Count2: ", count2 )
print ("Count3: ", count3 )
print (count2*count3)
        