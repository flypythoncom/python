#!/usr/bin env python

import socket,sys

s=socket.getaddrinfo(sys.argv[1],None,0,socket.SOCK_STREAM)

counter=0
for i in s:
  print "%d %s" % (counter,s[counter][4])
  counter += 1


