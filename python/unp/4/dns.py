#!/usr/bin env python

import sys,DNS

query=sys.argv[1]
DNS.DiscoverNameServers()

reqobj=DNS.Request()

answerobj=reqobj.req(name=query,qtype=DNS.Type.ANY)
if not len(answerobj.answers):
  print "not find"
for i in answerobj.answers:
  print "%-5s %s " % (i['typename'],i['data'])

