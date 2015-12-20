def displayType(num):
    print num, 'is',
    if isinstance(num,(int,long,float,complex)):
        print "a number of type:",type(num).__name__
    else:
        print "not a number at all"

displayType(2)
displayType(-1.9)
displayType(-1+1.9j)
displayType('xcxx')
