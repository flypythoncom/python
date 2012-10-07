#/usr/bin env python

import sys
print "welcome...."
print "please enter a string:"

sys.stdout.flush()
line=sys.stdin.readline().strip()


print "you enter the %s  is %d count" % (line,len(line)) 
