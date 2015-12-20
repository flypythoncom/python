print "Menu: input the choice\n"
print "s: sum"
print "a: avg"
print "x: exit"
aa =[1,2,3,4]
while True:
    ch = raw_input()
    if ch == 's':
        i = 0
        Sum = 0
        print "you choice sum:\n"
        for i in aa:
            Sum += i
        print Sum
    if ch == 'a':
        print "you choice avg:\n"
        i = 0
        Sum1 = 0
        for i in aa:
            Sum1 += i
        avg = float(Sum1)/(len(aa))
        print avg
    if ch == 'x':
        break
    
