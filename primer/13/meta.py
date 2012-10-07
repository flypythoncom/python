from warnings import warn

class ReqStr(type):
    def __init__(cls,name,bases,attrd):
        super(ReqStr,cls).__init__(name,bases,attrd)
        if "__str__" not in attrd:
            raise TypeError("class overring __str__")
        if "__repr__" not in attrd:
            warn("class suggests __repr__",stacklevel = 3)
print "define ReqStr (meta)class \n"

class Foo(object):
    __metaclass__ = ReqStr

    def __str__(self):
        return "instance of class",self.__class__.__name__
print "defined Foo class\n"

class Bar(object):
    __metaclass__ = ReqStr

    def __str__(self):
        return self.__class__.__name__
print "defined Bar class\n "

class FooBar(object):
    __metaclass__ = ReqStr
print "defined FooBar class \n"
