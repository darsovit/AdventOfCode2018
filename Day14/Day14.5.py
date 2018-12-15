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
state['scorematch'] = 0
state['scoreToMatch'] = bytearray()
state['scoreToMatch'] = [5, 8, 0, 7, 4, 1]

numRecipesToLeft = None
while not numRecipesToLeft:
    newRecipeScore = state['scores'][state['Alice']] + state['scores'][state['Bob']]
    scorestate = state['scorematch']
    if newRecipeScore > 9:
        print(1, end='')
        state['scores'].append(1)
        if 1 == state['scoreToMatch'][scorestate]:
            state['scorematch'] += 1
            if state['scorematch'] == len(state['scoreToMatch']):
                numRecipesToLeft = len(state['scores']) - len(state['scoreToMatch'])
        else:
            state['scorematch'] = 0
        newRecipeScore -= 10
    print(newRecipeScore, end='')
    state['scores'].append(newRecipeScore)
    if newRecipeScore == state['scoreToMatch'][scorestate]:
        state['scorematch'] += 1
        if state['scorematch'] == len(state['scoreToMatch']):
            numRecipesToLeft = len(state['scores']) - len(state['scoreToMatch'])
    else:
        state['scorematch'] = 0

    stepPosForAlice = state['Alice'] + 1 + state['scores'][state['Alice']]
    stepPosForBob   = state['Bob']   + 1 + state['scores'][state['Bob']]
    state['Alice'] = stepPosForAlice % len(state['scores'])
    state['Bob']   = stepPosForBob   % len(state['scores'])

print('')

print( numRecipesToLeft )