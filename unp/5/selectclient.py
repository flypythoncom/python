#!/usr/bin env python

import socket,sys,select
port=8888
host='localhost'

spinsize=10
spinpos=0
spindir=1

def spin():
  global spinsize,spinpos,spindir
  spinstr='.' * spinpos + '|' +'.'*(spinsize-spinpos-1)
  sys.stdout.write('r'+ spinstr + ' ')
  sys.stdout.flush()

  spinpos += spindir
  if spinpos < 0:
    spindir=1
    spinpos=1
  elif spinpos >= spinsize:
    spinpos -= 2
    spindir = -1

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

while 1:
  infds,outfds,errfds=select.select([s],[],[s],0.05)
  if len(infds):
    data=s.recv(4096)
  if not len(data):
    print "\rRemote end closed connection; exiting"
    break

  sys.stdout.write("\rRecived: " + data)
  sys.stdout.flush()

  if len(errfds):
    print "\r problem occurred; exiting"
    sys.exit(0)

spin()














