#!/usr/bin env python

import struct,sys

def htons(num):
  return struct.pack('!H',num)

def htonl(num):
  return struct.pack('!I',num)

def ntohs(data):
  return struct.unpack('!H',data)[0]

def ntohl(data):
  return struct.unpack("!I",data)[0]

def sendstring(data):
  return htonl(len(data)) + data

print "Enter a string:"
str=sys.stdin.readline().rstrip()

print repr(sendstring(str))
