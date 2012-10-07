
import os
for tmpdir in("/tmp"):
    if os.path.isdir(tmpdir):
        break
    else:
        print "no temp dir available"
        tmpdir = ""
if tmpdir:
        os.chdir(tmpdir)
        cwd = os.getcwd()
        print " current tmp dir"
        print cwd

        print "create example dir"
        os.mkdir("example")
        os.chdir("example")
        cwd = os.getcwd()
        print "new work dir"
        print  cwd
        print "list the dir"
        print os.listdir(cwd)

        print "create test file"
        fobj = open("test","w")
        fobj.write("xxg\n")
        fobj.write("111111")
        fobj.close()

        print "update the list dir"
        print os.listdir(cwd)

        print "rename the file"
        os.rename("test","xxg.txt")
        print os.listdir(cwd)

        
        
