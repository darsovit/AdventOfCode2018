#!python
'''
Advent of Code 2018, Day 13
https://adventofcode.com/2018/day/13
'''

def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f ) )

def getInput():
    return [
    '/->-\\',        
    '|   |  /----\\',
    '| /-+--+-\\  |',
    '| | |  | v  |',
    '\\-+-/  \\-+--/',
    '  \\------/',
    ]
    
def loadCartsAndFixLines( lines ):
    carts = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '<':
                assert( (y,x) not in carts )
                carts[(y,x)] = (0,-1,'l')
                #carts += [(y,x,0,-1,'l')]
                #cartsPos.add((y,x))
                lines[y] = lines[y][:x] + '-' + lines[y][x+1:]
                assert(lines[y][x-1] != ' ')
                assert(lines[y][x+1] != ' ')
            elif lines[y][x] == '>':
                assert( (y,x) not in carts )
                carts[(y,x)] = (0,1,'l')
                #carts += [(y,x,0,1,'l')]
                #cartsPos.add((y,x))
                lines[y] = lines[y][:x] + '-' + lines[y][x+1:]
                assert(lines[y][x-1] != ' ')
                assert(lines[y][x+1] != ' ')
            elif lines[y][x] == '^':
                assert( (y,x) not in carts )
                carts[(y,x)] = (-1,0,'l')
                #carts += [(y,x,-1,0,'l')]
                #cartsPos.add((y,x))
                lines[y] = lines[y][:x] + '|' + lines[y][x+1:]
                assert(lines[y+1][x] != ' ')
                assert(lines[y+1][x] != ' ')
            elif lines[y][x] == 'v':
                assert( (y,x) not in carts )
                carts[(y,x)] = (1,0,'l')
                #carts += [(y,x,1,0,'l')]
                #cartsPos.add((y,x))
                lines[y] = lines[y][:x] + '|' + lines[y][x+1:]
                assert(lines[y+1][x] != ' ')
                assert(lines[y-1][x] != ' ')
    return( carts, lines )

def runCarts( carts, lines ):
    nextCarts = {}
    moveCarts = list(carts.keys())
    moveCarts.sort()
    for cart in moveCarts:
        if cart in carts:
            (deltaY,deltaX,turnMem) = carts[cart]
            del carts[cart]
            newCartY = cart[0]+deltaY        
            newCartX = cart[1]+deltaX
            newTrack = lines[newCartY][newCartX]
            crashed = True
            if (newCartY,newCartX) in nextCarts:
                del nextCarts[(newCartY,newCartX)]
            elif (newCartY,newCartX) in carts:
                del carts[(newCartY,newCartX)]
            else:
                crashed = False
            if crashed:
                continue
            elif newTrack == '|' or newTrack == '-':            
                nextCarts[(newCartY,newCartX)] = (deltaY,deltaX,turnMem)
            elif newTrack == '\\':
                nextCarts[(newCartY,newCartX)] = (deltaX,deltaY,turnMem)
            elif newTrack == '/':
                nextCarts[(newCartY,newCartX)] = (-deltaX,-deltaY,turnMem)
            elif newTrack == '+':
                if turnMem == 'l':
                    nextCarts[(newCartY,newCartX)] = (-1*deltaX,deltaY,'s')                    
                elif turnMem == 's':
                    nextCarts[(newCartY,newCartX)] = (deltaY,deltaX,'r')
                else:
                    nextCarts[(newCartY,newCartX)] = (deltaX,-1*deltaY,'l')
                    assert( turnMem == 'r' )
            else:
                print( "cart off the rails???:", newTrack )
    return nextCarts

(carts,lines) = loadCartsAndFixLines( readInput() )

done = False
while not done:
    carts = runCarts( carts, lines )
    done = len(carts) == 1

print(carts)