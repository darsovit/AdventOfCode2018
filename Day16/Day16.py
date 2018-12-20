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
        program = []
        for line in list(map(str.rstrip, f.readlines())):
            if state == 0 and len(line) > 6 and "Before" == line[0:6]:
                state = 1
                beginVals = list( map(int, line[9:-1].split(', ') ) )
            elif state == 1:
                opInput = list( map(int, line.split(' ') ) )
                state = 2
            elif state == 2 and len(line) > 5 and 'After' == line[0:5]:
                afterVals = list( map(int, line[9:-1].split(', ') ) )
                samples += [{'begin':beginVals,'after':afterVals,'op':opInput}]
                state = 0
                beginVals = []
                opInput = []
            elif state == 0 and len(line) > 3:
                programOps = list(map(int, line.split(' ') ) )
                if len(programOps) == 4:
                    program += [ programOps ]
             
        return ( samples, program )        

def storeRegister( registers, c, val ):
    regList = list( registers )
    regList[c] = val
    return tuple( regList )
    
def addr(registers, a, b, c):
    return storeRegister( registers, c, registers[a] + registers[b] )

def addi(registers, a, b, c):
    return storeRegister( registers, c, registers[a] + b )

def mulr(registers, a, b, c):
    return storeRegister( registers, c, registers[a] * registers[b] )

def muli(registers, a, b, c):
    return storeRegister( registers, c, registers[a] * b )

def banr(registers, a, b, c):
    return storeRegister( registers, c, registers[a] & registers[b] )

def bani(registers, a, b, c):
    return storeRegister( registers, c, registers[a] & b )
    
def borr(registers, a, b, c):
    return storeRegister( registers, c, registers[a] | registers[b] )

def bori(registers, a, b, c):
    return storeRegister( registers, c, registers[a] | b )

def setr(registers, a, b, c):
    return storeRegister( registers, c, registers[a] )
    
def seti(registers, a, b, c):
    return storeRegister( registers, c, a )

def gtir(registers, a, b, c):
    return storeRegister( registers, c, 1 if a > registers[b] else 0 )

def gtri(registers, a, b, c):
    return storeRegister( registers, c, 1 if registers[a] > b else 0 )

def gtrr(registers, a, b, c):
    return storeRegister( registers, c, 1 if registers[a] > registers[b] else 0 )

def eqir(registers, a, b, c):
    return storeRegister( registers, c, 1 if a == registers[b] else 0 )

def eqri(registers, a, b, c):
    return storeRegister( registers, c, 1 if registers[a] == b else 0 )
    
def eqrr(registers, a, b, c):
    return storeRegister( registers, c, 1 if registers[a] == registers[b] else 0 )
    
test_funcs = [ addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr ]
( samples, program ) = readSamples()
countNumThreeOrMore = 0

for sample in samples:
    startRegisters = tuple( sample['begin'] )
    endRegisters   = tuple( sample['after'] )
    opInput        = sample['op']
    numTestsSuccessful = 0
    #print('Expected End: ', endRegisters )
    for test in test_funcs:
        testRegisters = startRegisters
        outRegisters = test( testRegisters, opInput[1], opInput[2], opInput[3])
        if outRegisters == endRegisters:
            #print('GOOD: input:', testRegisters, 'test:', test, 'ops:', opInput, 'output:', outRegisters )
            numTestsSuccessful += 1
        #else:
            #print('BAD : input:', testRegisters, 'test:', test, 'ops:', opInput, 'output:', outRegisters )
            
    if numTestsSuccessful >= 3:
        countNumThreeOrMore += 1
    #break
print( countNumThreeOrMore )
# First answer is too low (565)