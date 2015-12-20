#!/usr/bin env python

import socket

print "create socket"
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "done"

print "look up port number"
port=socket.getservbyname('http','tcp')
print "done"


print "connecting to the host on port %d" % port
s.connect(("www.baidu.com",port))
print  "done"

print "connected from",s.getsockname()
print "connected to",s.getpeername()
