#!python
'''
Advent of Code 2018, Day 14
https://adventofcode.com/2018/day/14
'''

state = {}
state['scores'] = bytearray()
state['scores'].append(3)
state['scores'].append(7)
state['Alice'] = 0
state['Bob'] = 1
while len( state['scores'] ) < 580752:
    newRecipeScore = state['scores'][state['Alice']] + state['scores'][state['Bob']]
    if newRecipeScore > 9:
        state['scores'].append(1)
        newRecipeScore -= 10
    state['scores'].append(newRecipeScore)
    stepPosForAlice = state['Alice'] + 1 + state['scores'][state['Alice']]
    stepPosForBob   = state['Bob']   + 1 + state['scores'][state['Bob']]
    state['Alice'] = stepPosForAlice % len(state['scores'])
    state['Bob']   = stepPosForBob   % len(state['scores'])

bytes = state['scores'][580741:580751]
print( ''.join( list( map( str, bytes )) ) )