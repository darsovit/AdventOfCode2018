#!python

A = 1
B = 0
C = 0
D = 0
E = 0

C = C+2
C = C*C
C = C*19
C = C*11
B = B+5
B = B*22
B = B+8
C = C+B

if ( A == 1 ):
    B = 27
    B = B * 28
    B = B + 29
    B = B * 30
    B = B * 14
    B = B * 32
    C = C + B
    A = 0
    
print ( A, B, C, D, E )

D = 1
while D <= C:
    E = 1
    divided = int( C / D )
    if (D * divided) == C:
        print( D, divided, C )
        A += divided
    #while E <= C:
    #    if (D*E) == C:
    #        A += D
    #    E += 1
    D += 1

print( A )

# 3273312 was too low ?