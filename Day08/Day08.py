#!python
'''
Advent of Code 2018, Day 8, Part 1
'''

def parseNode( data ):
    node = {}
    node['numChildren'] = data[0]
    node['numMetadata'] = data[1]
    node['children']    = []
    node['metadata']    = []
    consumed = 2
    for i in range(node['numChildren']):
        ( consumedByChild, childNode ) = parseNode(data[consumed:])
        node['children'] += [ childNode ]
        consumed += consumedByChild
    for i in range(node['numMetadata']):
        node['metadata'] += [ data[consumed+i] ]
    return ( consumed+node['numMetadata'], node )

def readInput():
    data = []
    with open('input.txt') as f:
        for line in f:
            data = list( map( int, line.rstrip().split(' ') ) )
    return data

def exampleInput():
    data = [ 2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2 ]
    return data

def addAllMetadata( node ):
    sumAllMetadata = 0
    for child in node['children']:
        sumAllMetadata += addAllMetadata(child)
    for metadata in node['metadata']:
        sumAllMetadata += metadata
    return sumAllMetadata

data = readInput()        
print( data )
(consumedPieces, rootNode) = parseNode( data )

print ( consumedPieces, len(data) )
print( addAllMetadata( rootNode ) )