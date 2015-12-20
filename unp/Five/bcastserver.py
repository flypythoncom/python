#!/usr/bin env python

import sys,socket

dest=('<broadcast>',8888)

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.sendto("hello",dest)

print "look for replies ...."
while 1:
  (buf,address)=s.recvfrom(2048)
  if not len(buf):
    break
  print "Recived from %s: %s" % (address,buf)
