#!python
'''
https://adventofcode.com/2018/day/1
'''
freq=0

with open('input.txt') as f:
    for line in f:
        freq += int(line)

print (freq)
