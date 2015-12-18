a = 19
print "please input a int number in 1-100"
x = raw_input()
while x != a:
    print "sorry error: \n input again:"
    x = raw_input()
if x == a:
    print "you are right"
    break
raw_input()
