
'readTextFile.py -- read and display text file'

#get filename
fname = raw_input("enter the filename:")
print

#attempt to open file for reading
try:
    fobj = open(fname,'r')
except IOError,e:
    print "*** file open error",e
else:
    #display contents to the screen
    for echoLine in fobj:
        print echoLine;
fobj.close()
