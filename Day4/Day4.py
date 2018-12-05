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
    guardId    = None
    entryDate  = None
    guardEntries = {}
    for log in logs:
        action = log.split()[2]
        if action == 'Guard':
            if guardEntry and entryDate:
                if guardId not in guardEntries:
                    guardEntries[guardId] = {}
                guardEntries[guardId][entryDate] = guardEntry
            (guardEntry, guardId, entryDate) = parseNewGuard( log )
            if guardId not in guardEntries:
                guardEntries[guardId] = {}
        elif action == 'falls':
            if guardEntry:
                guardEntry = parseGuardAsleep( guardEntry, log )
        elif action == 'wakes':
            if guardEntry:
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
    return (guardEntry, guardEntry['ID'], date)

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
    for guardId in guardDuties:
        totalSleep = 0
        for date in guardDuties[guardId]:
            guardDuty = guardDuties[guardId][date]
            #print( guardDuty )
            for (asleep,awake) in guardDuty['asleep']:
                totalSleep += ( awake - asleep )
            if guardDuty['state'] == 'asleep':
                print( "guard ended duty asleep" )
                totalSleep += 60 - int(guardDuty['priorStateSwap'])
        guardsAndSleepTimes[guardId] = totalSleep
    return guardsAndSleepTimes

def findLongestSleepingGuard( guardSleepTimes ):
    longestSleepGuardId = None
    longestSleepTime    = 0
    for guard in guardSleepTimes:
        if guardSleepTimes[guard] > longestSleepTime:
            longestSleepTime = guardSleepTimes[guard]
            longestSleepGuardId = guard
    return ( longestSleepGuardId )

def findLongestMinuteForGuard( guardDuties ):
    minuteCounts = {}
    for date in guardDuties:
        guardDuty = guardDuties[date]
        for (asleep,awake) in guardDuty['asleep']:
            for minute in range(asleep, awake):
                if minute in minuteCounts:
                    minuteCounts[minute] += 1
                else:
                    minuteCounts[minute] = 1
    highestMinuteAsleep = None
    highestMinuteCount  = None
    for minute in minuteCounts:
        if not highestMinuteCount:
            highestMinuteAsleep = minute
            highestMinuteCount = minuteCounts[minute]
        elif highestMinuteCount < minuteCounts[minute]:
            highestMinuteAsleep = minute
            highestMinuteCount = minuteCounts[minute]
    return highestMinuteAsleep
        

sortedInput = loadAndSortInput()
guardDuties = parseGuardDuties( sortedInput )
guardSleepTimes = countGuardAndSleepTimes( guardDuties )
longestSleepGuard = findLongestSleepingGuard( guardSleepTimes )
longestMinuteForGuard = findLongestMinuteForGuard( guardDuties[longestSleepGuard] )
print( longestSleepGuard, longestMinuteForGuard, longestSleepGuard * longestMinuteForGuard )