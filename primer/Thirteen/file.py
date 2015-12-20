import os
import pickle

class File(object):
    saved=[]
    def __init__(self,name=None):
        self.name = name
    def __get__(self,obj,typ=None):
        if self.name not in File.saved:
            raise AttributeError,"%r used before assignment " % self.name
        try:
            f = open(self.name,"r")
            val = pickle.load(f)
            f.close()
            return val
        except (pickle.UnpicklingError,IOError,EOFError,AttributeError,\
                ImportError,IndexError),e:
            raise AttributeError,"could not read %r:%s" % (self.name,e)
    def __set__(self,obj,val):
        f = open(self.name,"w")
        try:
            pickle.dump(val,f)
            File.saved.append(self.name)
        except (TypeError,pickle.PicklingError),e:
             raise AttributeError,"could not pickle %r " % self.name
        finally:
            f.close()
                
    def __delete__(self,obj):
        try:
            os.unlink(self.name)
            File.saved.remove(self.name)
        except (OSError,ValueError),e:
            pass
