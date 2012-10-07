#!/usr/bin/env python
# --coding: utf-8 --
#简单的Gopher Client

import socket,sys

port = 70          #默认端口 70
host = sys.argv[1]
filename = sys.argv[2]

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

fd = s.makefile('rw',0)

fd.write(filename + "\r\n")

for line in fd.readline():
  sys.stdout.write(line)








