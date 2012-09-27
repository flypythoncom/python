import os

filename=raw_input("filename:")
if os.path.exists(filename):
    print "file exist"
    exit()


fd=open(filename,'r')
fd.writelines(all)
fd.close()

print "done"

