#!/usr/bin env python

import sys,socket

host='localhost'
port=8888

data="x"*1024

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

bytewritten=0
while bytewritten < len(data):
  startpos=bytewritten
  endpos=min(bytewritten + 1024,len(data))
  bytewritten += s.send(data[startpos:endpos])
  sys.stdout.write("write %d bytes\r" % bytewritten)
  sys.stdout.flush()

s.shutdown(1)

print "All data sent"
while 1:
  buf=s.recv(1024)
  if not len(buf):
    break
  sys.stdout.write(buf)


