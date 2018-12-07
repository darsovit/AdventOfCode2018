#!python
'''
Advent of Code 2018, Day 6, Part 2
'''

def readInputCoords():
    coords = []
    with open('input.txt') as f:
        for line in f:
            (x,y) = map(int, line.split(', '))
            coords += [(x,y)]
    return coords

def findCenter( coords ):
    (maxX, maxY) = coords[0]
    (minX, minY) = coords[0]
    for (x,y) in coords:
        maxX = x if x > maxX else maxX
        maxY = y if y > maxY else maxY
        minX = x if x < minX else minX
        minY = y if y < minY else minY
    midX = int((maxX+minX)/2)
    midY = int((maxY+minY)/2)
    return (midX,midY)


class BuildManhattanDistanceField:
    def __init__(self, coords, maxDistance):
        self.coords = coords
        self.field  = {}
        self.seed   = []
        self.maxSumDist = maxDistance
        self.fieldSize = 0

    def calculateManhattanDistanceSumToCoords( self, pos ):
        manhattanDistanceSum = 0
        for (x,y) in self.coords:
            manhattanDistanceSum += abs(pos[0]-x) + abs(pos[1]-y)
        return manhattanDistanceSum

    def growField(self):
        new_seed = []
        deltas = [(1,0),(-1,0),(0,1),(0,-1)]
        for pos in self.seed:
            for delta in deltas:
                newPos = ( pos[0]+delta[0], pos[1]+delta[1] )
                if newPos not in self.field:
                    distance = self.calculateManhattanDistanceSumToCoords( newPos )
                    self.field[newPos] = distance
                    if distance < self.maxSumDist:
                        new_seed += [newPos]

        self.seed = new_seed
        self.fieldSize += len(self.seed)
        return len(self.seed) == 0
            
            
    def calculateFieldFromCenter( self, center ):
        # Luckily, we don't have to find the start of the field
        distance = self.calculateManhattanDistanceSumToCoords( center )
        self.field[center] = distance
        self.seed += [center]
        self.fieldSize += 1
        done = False
        while not done:
            done = self.growField()
        return self.fieldSize
        

coords = readInputCoords()

fieldFinder = BuildManhattanDistanceField( coords, 10000 )
middleOfField = findCenter( coords )
size = fieldFinder.calculateFieldFromCenter( middleOfField )
print ( size )