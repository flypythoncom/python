'''
An example for unicode string
'''

CODEC = "utf-8"
FILE = "unicode.txt"

hello = u"hhhh\n"
byte = hello.encode(CODEC)
f = open(FILE,"w")
f.write(byte)
f.close()

f = open(FILE,"r")
byte = f.read()
f.close()

hello = byte.decode(CODEC)
print hello
raw_input()
