#! /usr/bin env python

import socket

host=''
porr=51423

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,porr))
s.listen(1)

print "server is runing on port %d" % port

while 1:
  clientsock,clientaddr=s.accept()
  clientfile=clientsock.makefile('rw',0)
  clientfile.write("welcome," + str(clientaddr) + "\n")
  clientfile.write("please enter a string:")
  line = clientfile.readline().strip()
  clientfile.write("you enter %d char"  % len(line)  )
  clientfile.close()
  clientsock.close()


