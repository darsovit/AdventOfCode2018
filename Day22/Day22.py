#!python
'''
Advent of Code 2018, Day 22
https://adventofcode.com/2018/day/22
'''

def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )

def sampleInput():
    return [
        'depth: 510',
        'target: 10,10'
    ]

class region:
    def __init__(self, pos, depth, left=None, above=None, target=False):
        self.symbol = None
        if pos[0] == 0 and pos[1] == 0:
            self.geo_index = 0
            self.symbol    = 'M'
        elif target:
            self.geo_index = 0
            self.symbol    = 'T'
        elif pos[1] == 0:
            self.geo_index = pos[0] * 16807
        elif pos[0] == 0:
            self.geo_index = pos[1] * 48271
        else:
            self.geo_index = left.getErosionLevel() * above.getErosionLevel()
        self.erosion_level = ( self.geo_index + depth ) % 20183
        self.type          = self.erosion_level % 3
        if not self.symbol:
            if self.type == 0:
                self.symbol = '.'
            elif self.type == 1:
                self.symbol = '='
            elif self.type == 2:
                self.symbol = '|'
        
    def getErosionLevel(self):
        return self.erosion_level
        
    def getSymbol(self):
        return self.symbol
    def getTypeValue(self):
        return self.type
            
class geologic:
    def __init__(self, lines):
        self.depth = int( lines[0].split(' ')[1] )
        self.pos   = tuple( map( int, lines[1].split(' ')[1].split(',') ) )
        self.field = []
        self.field.append([])        
        self.field[0].append(region( (0,0), self.depth ) )

        for x in range(1, self.pos[0]+1 ):
            self.field[0].append( region( (x, 0), self.depth, left = self.field[0][x-1] ) )
        for y in range(1,self.pos[1]):
            self.field.append([])
            self.field[y].append( region( (0, y), self.depth ) )
            for x in range(1, self.pos[0]+1):
                self.field[y].append( region((x,y), self.depth, left=self.field[y][x-1], above=self.field[y-1][x] ) )
        for y in range( self.pos[1], self.pos[1]+1 ):
            self.field.append([])
            self.field[y].append( region( (0, y), self.depth ) )
            for x in range( 1, self.pos[0] ):
                self.field[y].append( region( (x,y), self.depth, left=self.field[y][x-1], above=self.field[y-1][x] ) )
            for x in range( self.pos[0], self.pos[0]+1 ):
                self.field[y].append( region( (x,y), self.depth, target=True ) )
        
    def debugPrint(self):
        print( self.pos, self.depth )
        for y in range( self.pos[1]+1 ):
            for x in range( self.pos[0] + 1 ):
                print( self.field[y][x].getSymbol(), end='' )
            print()
        
    def calculateRiskInRectangleToTarget( self ):
        risk = 0
        for y in range( self.pos[1] + 1 ):
            for x in range( self.pos[0] + 1 ):
                risk += self.field[y][x].getTypeValue()
        return risk
        
caves = geologic( readInput() )
caves.debugPrint()
print( 'total risk:', caves.calculateRiskInRectangleToTarget() )