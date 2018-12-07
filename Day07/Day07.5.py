#!python
'''
Advent of Code 2018, Day 7, 1st Solution
https://adventofcode.com/2018/day/7
'''

def readInputGraph():
    graph = {}
    graph['edges'] = []
    graph['nodes'] = set()
    with open('input.txt') as f:
        for line in f:
            parts = line.split(' ')
            startNode = parts[1]
            endNode   = parts[7]
            graph['edges'] += [(startNode,endNode)]
            if startNode not in graph['nodes']:
                graph['nodes'].add(startNode)
            if endNode not in graph['nodes']:
                graph['nodes'].add(endNode)
    return graph
    
print( readInputGraph() )
            