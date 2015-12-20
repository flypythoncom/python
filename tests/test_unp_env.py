#!/usr/bin/python
import unittest
import sys,socket
import os

pwd = os.path.dirname(os.path.realpath(__file__))
print pwd
base_dir = os.path.join(pwd,'..')
print base_dir

sys.path.append(base_dir)
# expand/__init__.py has to be added into Four(4) dir
# 4 changed to Four due to the fact it cannot be as a package name in python
# I never use this way in any other languages, I guess it have to be changed eventually

# this way  - same function in different package can be avoided
# but I really do not like to type or read this many
# gliang Dec 20 2015
import unp.Four.environment

class primerTest11(unittest.TestCase):
    def test_convert(self):
        
        hostname=socket.gethostname()
        self.assertNotEqual(hostname,"www.ipursuit.caa")
        self.assertNotEqual(unp.Four.environment.getipaddrs(hostname),"192.168.0.1")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(primerTest11)
    unittest.TextTestRunner(verbosity=2).run(suite)




# try to add unittest for exception later, do not remove it for now 
#print "full-name:",socket.getfqdn(hostname)
#try:
#  print "IP address:",", ".join(getipaddrs(hostname))
#except socket.gaierror,e:
#  print "can not get ip address",e

