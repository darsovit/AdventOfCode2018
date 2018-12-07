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

def runGraph( numWorkers, graph ):
    runOrder = []
    ticks = 0
    jobsProgressing = {}

    while len( graph['runnable'] ) > 0 or len(jobsProgressing) > 0:
        runnableList = list(graph['runnable'])
        runnableList.sort()
        while len(jobsProgressing) < numWorkers and len(runnableList) > 0:
            nodeToRun = runnableList.pop(0)
            jobsProgressing[nodeToRun] = ord(nodeToRun) - ord('A') + 61            
            graph['runnable'].remove(nodeToRun)

        ticks += 1
        jobsToRemove = []
        for job in jobsProgressing:
            jobsProgressing[job] -= 1
            if jobsProgressing[job] == 0:
                jobsToRemove += [job]
                if job in graph['dependees']:
                    for nodeMaybeRunnable in graph['dependees'][job]:
                        graph['dependencies'][nodeMaybeRunnable].remove(job)
                        if len(graph['dependencies'][nodeMaybeRunnable]) == 0:
                            graph['runnable'].add( nodeMaybeRunnable )
        for job in jobsToRemove:
            del jobsProgressing[job]
    return ticks

graph = readInputGraph()
graph = buildRunnableGraph( graph )
print( runGraph(5, graph) )
      