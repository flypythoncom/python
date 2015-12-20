#!/usr/bin env python

import sys,socket

try:

  s=socket.gethostbyaddr(sys.argv[1])

  print "hostname:"
  print " "+ s[0]

  print "\nAddress:"
  for i in s[2]:
    print " " + i

except socket.herror,e:
  print "can not look up name:",e


