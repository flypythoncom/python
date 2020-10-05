import os


#Opens youtube link in browser.
if os.name == "nt":
	try:
		os.system("start chrome https://www.youtube.com/watch?v=_uQrJ0TkZlc&list=PLTjRvDozrdlxj5wgH4qkvwSOdHLOCx10f")
	except:
		os.system("start iexplore https://www.youtube.com/watch?v=_uQrJ0TkZlc&list=PLTjRvDozrdlxj5wgH4qkvwSOdHLOCx10f")
else:
	try:
		os.system("firefox https://www.youtube.com/watch?v=_uQrJ0TkZlc&list=PLTjRvDozrdlxj5wgH4qkvwSOdHLOCx10f")
	except:
		os.system("open -a Safari https://www.youtube.com/watch?v=_uQrJ0TkZlc&list=PLTjRvDozrdlxj5wgH4qkvwSOdHLOCx10f")
