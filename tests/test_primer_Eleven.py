#!/usr/bin/python
import unittest

import sys,os
pwd = os.path.dirname(os.path.realpath(__file__))
print pwd
base_dir = os.path.join(pwd,'..')
print base_dir

sys.path.append(base_dir)
# expand/__init__.py has to be present for this to work
import primer.Eleven.numconv 

class primerTest11(unittest.TestCase):
    def test_convert(self):
        myseq=(123,45.67,-6.2e8,99999999L)
        int_seq=[123,45,-620000000,99999999]
        self.assertEqual(primer.Eleven.numconv.convert(int,myseq), int_seq)
        self.assertEqual(primer.Eleven.numconv.convert(long,myseq), int_seq)
        self.assertNotEqual(primer.Eleven.numconv.convert(float,myseq), int_seq)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(primerTest11)
    unittest.TextTestRunner(verbosity=2).run(suite)

