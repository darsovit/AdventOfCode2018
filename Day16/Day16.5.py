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
    
def determineOpCodes( samples ):
    testOpCodes = {}
    test_funcs = set( [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr] )
    for sample in samples:
        opCode = sample['op'][0]
        if opCode not in testOpCodes:
            testOpCodes[opCode] = set(test_funcs)
    for sample in samples:
        startRegisters = tuple(sample['begin'])
        endRegisters   = tuple(sample['after'])
        opInput        = sample['op']
        opCode         = opInput[0]
        removeFromPossibleOpCodes = []
        for test in testOpCodes[opCode]:
            outRegisters = test( startRegisters, opInput[1], opInput[2], opInput[3] )
            if outRegisters != endRegisters:
                removeFromPossibleOpCodes += [ test ]
        for removeTest in removeFromPossibleOpCodes:
            testOpCodes[opCode].remove( removeTest )
        assert len( testOpCodes[opCode] ) > 0
    opCodes = {}
    while len(testOpCodes) > 0:
        opsToRemoveFromTestOpCodes = []
        determinedFuncs = set()
        for opCode in testOpCodes.keys():
            if len(testOpCodes[opCode]) == 1:
                opCodes[opCode] = next(iter(testOpCodes[opCode]))
                test_funcs.remove( opCodes[opCode] )
                determinedFuncs.add( opCodes[opCode] )
                opsToRemoveFromTestOpCodes += [ opCode ]
        funcMap = {}
        for opCode in testOpCodes.keys():
            for func in testOpCodes[opCode]:
                if func not in funcMap:
                    funcMap[func] = set()
                funcMap[func].add( opCode )
        for func in funcMap:
            if len(funcMap[func]) == 1:
                opCode = next(iter(funcMap[func]))
                opCodes[opCode] = func
                test_funcs.remove(opCodes[opCode] )
                determinedFuncs.add( opCodes[opCode] )
                opsToRemoveFromTestOpCodes += [ opCode ]
        for foundOp in opsToRemoveFromTestOpCodes:
            del testOpCodes[foundOp]
            assert foundOp not in testOpCodes.keys()
        for opCode in testOpCodes.keys():
            testOpCodes[opCode] = testOpCodes[opCode].difference( determinedFuncs )
    assert len(test_funcs) == 0
    return opCodes
    
    
def runProgram( opCodes, program ):
    registers = (0,0,0,0)
    for line in program:
        (opCode,a,b,c) = line
        assert opCode in opCodes
        registers = opCodes[opCode](registers, a,b,c)
    return registers

( samples, program ) = readSamples()
opCodes = determineOpCodes( samples )
registers = runProgram( opCodes, program )
print( registers )