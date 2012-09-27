#!/usr/bin env pythhon

import sys,socket

def getipaddrs(hostname):
  s=socket.getaddrinfo(hostname,None,0,socket.SOCK_STREAM)
  return [x[4][0] for x in s]

hostname=socket.gethostname()
print "Host name:",hostname

print "full-name:",socket.getfqdn(hostname)
try:
  print "IP address:",", ".join(getipaddrs(hostname))
except socket.gaierror,e:
  print "can not get ip address",e

