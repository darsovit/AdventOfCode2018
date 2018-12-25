#! python

D = 0x10000
A = 0x1000000
setOfDs = set()
lastAnswer = None
repeatCount = 0
while not D == A:
    C = D | 0x10000
    D = 10552971
    while True:
        E = C & 0xFF
        D = D + E
        D = D & 0xFFFFFF
        D = D * 65899
        D = D & 0xFFFFFF
        if ( 256 > C ):
            break
        E = 0
        while (E+1)*256 <= C:
            E += 1
        C = E
    print( D )
    if not lastAnswer:
        lastAnswer = D
        setOfDs.add( D )
    elif D in setOfDs:
        print( 'Repeated D:', D, ' -- last answer not repeated: ', lastAnswer )
        repeatCount += 1
        if repeatCount > 10:
            A = D
    else:
        setOfDs.add( D )
        lastAnswer = D