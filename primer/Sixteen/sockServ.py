from SocketServer import (TCPServer as TCP,
    StreamRequestHandler as SRH)
from time import ctime

HOST=''
PORT=8888
ADDR=(HOST,PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print "......connected from :",self.client_address
        self.wfile.write('[%s] %s' %
                         (ctime(),self.rfile.readline()))

tcpSer = TCP(ADDR,MyRequestHandler)
print "waiting for connection..."
tcpSer.serve_forever()
