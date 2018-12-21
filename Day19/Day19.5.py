#!python
'''
Advent of Code 2018, Day 19
https://adventofcode.com/2018/day/19
'''

def sampleInput():
    return [
        "#ip 0",
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5"
    ]
    
def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )

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

def getOp(opName):
    ops = { 'addr': addr, 'addi': addi, 'mulr': mulr, 'muli': muli,
            'banr': banr, 'bani': bani, 'borr': borr, 'bori': bori,
            'setr': setr, 'seti': seti, 
            'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
            'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr }
    assert opName in ops, 'Failed to find op'
    return ops[opName]

def determineIp( line ):
    parts = line.split(' ')
    assert parts[0] == '#ip'
    return int(parts[1])
    
def runStep( registers, instruction ):
    return instruction[0]( registers, instruction[1], instruction[2], instruction[3] )

class timemachine:
    def __init__(self, input, registers=(0,0,0,0,0,0)):
        self.cpu = {}
        self.cpu['registers'] = registers
        self.cpu['ip'] = determineIp( input[0] )
        self.program = []
        for line in input[1:]:
            instruction = line.split(' ')
            self.program += [ ( getOp(instruction[0]), int(instruction[1]), int(instruction[2]), int(instruction[3]) ) ]
    
    def debugPrint(self):
        print('program:')
        for line in self.program:
            print( line )
        print('registers:', self.cpu['registers'] )
        print( 'ip bound to register:', self.cpu['ip'] )
    
    def getInstruction(self):
        ipValue = self.cpu['registers'][self.cpu['ip']]
        return self.program[ipValue]

    def incrementIp(self):
        self.cpu['registers'] = storeRegister( self.cpu['registers'], self.cpu['ip'], self.cpu['registers'][self.cpu['ip']] + 1 )

    def runProgram( self ):
        while ( self.cpu['registers'][self.cpu['ip']] < len(self.program) ):
            self.cpu['registers'] = runStep( self.cpu['registers'], self.getInstruction() )
            self.incrementIp()
            
tardis = timemachine( readInput(), registers=(1,0,0,0,0,0) )
tardis.debugPrint()
tardis.runProgram()
tardis.debugPrint()