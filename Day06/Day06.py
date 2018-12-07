#!python
'''
Advent of Code, Day 6, Part 1
'''

def readInputCoords():
    coords = []
    with open('input.txt') as f:
        for line in f:
            (x,y) = map(int, line.split(', '))
            coords += [(x,y)]
    return coords

class ManhattanClosestDistance:
    def __init__( self, coords ):
        self.field = {}
        self.seed  = []
        self.coords = coords
        self.gen  = 0
        self.last_growth = {}
        self.last_totalgrowth = 0
        self.totalgrowthOfFourInArow = 0
        for id in range(len(coords)):
            ( x, y ) = coords[id]
            self.field[(x,y)] = ( id, 0 )
            self.seed += [ (x,y,id) ]
            
    def dump( self ):
        print ( self.field )
        print ( self.seed )

    def expand( self ):
        done = False
        while not done:
            done = self.process()

    
    def process( self ):
        next_seed  = []
        self.gen  += 1
        deltas = [(1,0),(-1,0),(0,1),(0,-1)]
        growth = {}
        growth[-1] = 0
        totalgrowth = 0
        print( "growth:", growth )
        for (x,y,id) in self.seed:
            if id not in growth:
                growth[id] = 0
            if self.field[(x,y)][0] == id:
                for delta in deltas:
                    newX = x+delta[0]
                    newY = y+delta[1]
                    if (newX, newY) not in self.field:
                        next_seed += [ (newX,newY,id) ]
                        self.field[(newX,newY)] = (id, self.gen)
                        if id == 0:
                            print("Incrementing 0's growth")
                        growth[id] += 1
                        totalgrowth += 1
                    else:
                        (foundId, foundGen) = self.field[(newX,newY)]
                        if foundGen == self.gen and foundId != id and foundId != -1:
                            if foundId not in growth:
                                print("foundId not found in growth, somehow: ", foundId )
                            growth[foundId] += -1
                            growth[-1] += 1
                            self.field[(newX,newY)] = (-1, self.gen)
                  
        print("growth after process: ", growth)
        print("total growth: ", totalgrowth )
        if growth == self.last_growth:
            print( growth )
            print (self.last_growth)
            print ("last seed:", self.seed)
            print ("new seed:", next_seed)
            print("Finished in generation: ", self.gen )
            return True
        self.seed = next_seed
        self.last_growth = growth
        if (self.last_totalgrowth + 4 == totalgrowth ):
            self.totalgrowthOfFourInArow += 1
        else:
            self.totalgrowthOfFourInArow = 0
        self.last_totalgrowth = totalgrowth
        return self.totalgrowthOfFourInArow > 4

    def findBiggestStaticIdAndSize( self ):
        largestStaticId = None
        largestStaticSize = None
        staticSize = {}
        
        for (x,y) in self.field:
            (id, gen) = self.field[(x,y)]
            if id not in self.last_growth:
                if id not in staticSize:
                    staticSize[id] = 0
                staticSize[id] += 1
        
        largestStaticId = None
        largestStaticSize = None
        for id in staticSize:
            if not largestStaticSize:
                largestStaticSize = staticSize[id]
                largestStaticId   = id
            elif staticSize[id] > largestStaticSize:
                largestStaticSize = staticSize[id]
                largestStaticId   = id
        return (id, largestStaticSize)
        
coords = readInputCoords()
finder = ManhattanClosestDistance( coords )
finder.expand()
(id, size) = finder.findBiggestStaticIdAndSize()
print( id, size )
#finder.dump()