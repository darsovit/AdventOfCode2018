#! python

D = 0x10000
A = 0x1000000
setOfDs = set()
lastAnswer = None
firstAnswer = None
repeatCount = 0
while not D == A:
    C = D | 0x10000
    D = 10552971
    while True:

        D = D + ( C & 0xFF )
        D = D & 0xFFFFFF
        D = D * 65899
        D = D & 0xFFFFFF
        if ( 256 > C ):
            break
        C = int( C / 256 )
    #print( D )
    if not lastAnswer:
        lastAnswer = D
        firstAnswer = D
        setOfDs.add( D )
    elif D in setOfDs:
        #print( 'Repeated D:', D, ' -- last answer not repeated: ', lastAnswer )
        repeatCount += 1
        if repeatCount > 10:
            A = D
    else:
        setOfDs.add( D )
        lastAnswer = D
print( 'First:', firstAnswer )
print( 'Last non-repeated:', lastAnswer )