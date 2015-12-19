#!/usr/bin/python
import unittest

import sys,os
pwd = os.path.dirname(os.path.realpath(__file__))
print pwd
base_dir = os.path.join(pwd,'..')
print base_dir

sys.path.append(base_dir)
# expand/__init__.py has to be present for this to work
from expand import replace_str
from expand import randintEx
class expandTest(unittest.TestCase):
    def test_re(self):
        self.assertEqual(replace_str.printReplace('xxx','zz'),'xxx')


if __name__ == '__main__':
    unittest.main()
