#!/usr/bin/env python

import urllib,sys

f=urllib.urlopen(sys.argv[1])

while True:
  buf = f.read(2048)
  if not len(buf):
    break
  sys.stdout.write(buf)
