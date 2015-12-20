#!/usr/bin env python

import socket,sys

host=sys.argv[1]
textport=sys.argv[2]
filename=sys.argv[3]

try:
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error,e:
  print "strange erroe create socket %s" % e
  sys.exit(1)


try:
  port = int(textport)
except ValueError:
  try:
    port=socket.getservbyname(textport,'tcp')
  except socket.error,e:
    print "could find you port %s" % e
    sys.exit(1)

