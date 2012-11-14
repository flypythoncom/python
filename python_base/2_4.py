#验证用户名和PIN码

database = [
		['hello','1'],
		['world','2'],
		['!','3']
	  ]

username = raw_input("input the user name:")
pin      = raw_input("input tne user pin:")

if [username,pin] in database:
	print "Access greanted"
else:
        print "Error pin code or username"

