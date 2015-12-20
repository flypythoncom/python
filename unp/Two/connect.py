#!/usr/bin env python

import socket

print "create socket"
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "done"


print "connecting to the host"
s.connect(('localhost',8888))
print  "done"
