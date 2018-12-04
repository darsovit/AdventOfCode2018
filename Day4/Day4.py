#!python
'''
Advent of Code, Day 4, Problem 1
https://adventofcode.com/2018/day/4
'''

def loadAndSortInput():
    inputLines = []
    with open('input.txt') as f:
        for line in f:
            inputLines += [ line.rstrip() ]
    inputLines.sort()
    return inputLines

def parseGuardDuties( logs ):
    guardEntry = None
    entryDate  = None
    guardEntries = {}
    for log in logs:
        action = log.split()[2]
        if action == 'Guard':
            if guardEntry and entryDate:
                guardEntries[entryDate] = guardEntry
            (guardEntry, entryDate) = parseNewGuard( log )
        elif action == 'falls':
            if guardEntry and entryDate:
                guardEntry = parseGuardAsleep( guardEntry, log )
        elif action == 'wakes':
            if guardEntry and entryDate:
                guardEntry = parseGuardAwake( guardEntry, log )
    return guardEntries

def parseNewGuard( log ):
    ( date, time, restOfLog ) = parseDateAndTime( log )
    guardId = restOfLog.split()[1]
    hour = time.split(':')[0]
    if hour == '23':
        date = incrementDate( date )
    guardEntry = {}
    guardEntry['ID'] = int( guardId[1:] )
    guardEntry['log'] = [ log ]
    guardEntry['date'] = date
    guardEntry['state'] = 'awake'
    guardEntry['priorStateSwap'] = 0
    guardEntry['awake'] = []
    guardEntry['asleep'] = []
    return (guardEntry, date)

def parseGuardAsleep( guardEntry, log ):
    ( date, time, restOfLog ) = parseDateAndTime( log )
    minute = time.split(':')[1]
    if guardEntry['state'] == 'awake':
        guardEntry['awake'] += [(int(guardEntry['priorStateSwap']), int(minute))]
    guardEntry['state'] = 'asleep'
    guardEntry['priorStateSwap'] = minute
    guardEntry['log'] += [ log ]
    return guardEntry

def parseGuardAwake( guardEntry, log ):
    ( date, time, restOfLog ) = parseDateAndTime( log )
    minute = time.split(':')[1]
    if guardEntry['state'] == 'asleep':
        guardEntry['asleep'] += [(int(guardEntry['priorStateSwap']), int(minute))]
    guardEntry['state'] = 'awake'
    guardEntry['priorStateSwap'] = minute
    guardEntry['log'] += [ log ]
    return guardEntry

def parseDateAndTime( log ):
    splitLog = log.split()
    date = splitLog[0][1:]
    time = splitLog[1][:-1]
    restOfLog = ' '.join(splitLog[2:])
    #print ('parsed date, time, restOfLog:', date, time, restOfLog )
    return (date, time, restOfLog)

def incrementDate( date ):
    splitDate = date.split('-')
    splitDate[2] = str( int(splitDate[2]) + 1 )
    return '-'.join( splitDate )

def countGuardAndSleepTimes( guardDuties ):
    guardsAndSleepTimes = {}
    for date in guardDuties:
        guardDuty = guardDuties[date]
        print( guardDuty )
        totalSleep = 0
        for (asleep,awake) in guardDuty['asleep']:
            totalSleep += ( awake - asleep )
        if guardDuty['state'] == 'asleep':
            print( "guard ended duty asleep" )
            totalSleep += 60 - int(guardDuty['priorStateSwap'])
        if guardDuty['ID'] not in guardsAndSleepTimes.keys():
            guardsAndSleepTimes[guardDuty['ID']] = 0
        guardsAndSleepTimes[guardDuty['ID']] += totalSleep
    return guardsAndSleepTimes

def findLongestSleepingGuard( guardSleepTimes ):
    longestSleepGuardId = None
    longestSleepTime    = 0
    for guard in guardSleepTimes:
        if guardSleepTimes[guard] > longestSleepTime:
            longestSleepTime = guardSleepTimes[guard]
            longestSleepGuardId = guard
    return ( longestSleepGuardId, longestSleepTime )

sortedInput = loadAndSortInput()
guardDuties = parseGuardDuties( sortedInput )
guardSleepTimes = countGuardAndSleepTimes( guardDuties )
longestSleepGuard = findLongestSleepingGuard( guardSleepTimes )
print( longestSleepGuard[0] * longestSleepGuard[1] )