#!python
'''
Second problem for day 1
https://adventofcode.com/2018/day/1
'''
def input_freq_file(_freq, _freqs):
    with open('input.txt') as f:
        for line in f:
            this_freq = int(line)
            _freq += this_freq
            if _freq in freqs:
                print ("Found duplicate frequency: %s" % _freq)
                return ( True, _freq )
            else:
                #print ("Adjustment: %s, Frequency: %s" % (line, _freq) )
                _freqs.add(_freq)
    return ( False, _freq )
    

freq=0
freqs=set()
done = False

while not done:
    (done, freq) = input_freq_file(freq, freqs)
    #print( freqs )


# 13 is not right, what was done wrong
