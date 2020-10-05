import os

if os.name == "nt":
	try:
		os.system("start chrome")
	except:
		os.system("start iexplore")
else:
	try:
		os.system("firefox")
	except:
		os.system("open -a Safari")
