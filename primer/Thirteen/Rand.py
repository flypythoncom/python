
from random import choice

class Rand(object):
    def _init_(self,seq):
        self.data = seq
    def _iter_(self):
        return self
    def next(self):
        return choice(self.data)
