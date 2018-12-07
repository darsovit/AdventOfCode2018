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

def buildRunnableGraph( graph ):
    graph['runnable'] = set()
    for node in graph['nodes']:
        graph['runnable'].add(node)
    graph['dependencies'] = {}
    graph['dependees']    = {}    
    for edge in graph['edges']:
        if edge[1] in graph['runnable']:
            graph['runnable'].remove(edge[1])
        if edge[1] not in graph['dependencies']:
            graph['dependencies'][edge[1]] = set()
        graph['dependencies'][edge[1]].add(edge[0])
        if edge[0] not in graph['dependees']:
            graph['dependees'][edge[0]] = set()
        graph['dependees'][edge[0]].add(edge[1])
    return graph

def runGraph( graph ):
    runOrder = []
    while len( graph['runnable'] ) > 0:
        runnableList = list(graph['runnable'])
        runnableList.sort()
        nodeToRun = runnableList[0]
        runOrder += [nodeToRun]
        graph['runnable'].remove(nodeToRun)

        if nodeToRun in graph['dependees']:
            for nodeMaybeCleared in graph['dependees'][nodeToRun]:
                graph['dependencies'][nodeMaybeCleared].remove(nodeToRun)
                if len(graph['dependencies'][nodeMaybeCleared]) == 0:
                    graph['runnable'].add( nodeMaybeCleared )
    return ''.join(runOrder)

graph = readInputGraph()
graph = buildRunnableGraph( graph )
print( runGraph(graph) )
      