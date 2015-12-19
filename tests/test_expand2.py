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
    def test_printReplace(self):
        word = 'i'
        input_str = 'xxx'
        expected = 'xxx'
        result = replace_str.printReplace(input_str,word)
        self.assertEqual(result, expected, msg = None)
        self.assertEqual(replace_str.printReplace('xxxi','zz'),'xxxi')
    def test_printReplace_re(self):
        self.assertEqual(replace_str.printReplace_re('xxx','zz'),'xxx')
        self.assertEqual(replace_str.printReplace_re('xxxi','zz'),'xxxi')


if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(expandTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
