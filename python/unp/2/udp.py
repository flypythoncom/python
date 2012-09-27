#! /usr/bin env python

import socket,sys

host=sys.argv[1]
textport=sys.argv[2]

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

try:
  port=int(textport)
except ValueError:
  port=socket.getservbyname(textport,'udp')


s.connect((host,port))

print "enter data to tranmit:"

data=sys.stdin.readline().strip()
s.sendall(data)

print "looking for replies;"

while 1:
  buf=s.recv(2048)
  if not len(buf):
    break
  sys.stdout.write(buf)


