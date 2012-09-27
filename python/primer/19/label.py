import Tkinter

top = Tkinter.Tk()

label = Tkinter.Label(top,text="input")
label.pack()

button = Tkinter.Button(top,text="QIUT",command=top.quit,bg="red",fg="white")
button.pack(fill=Tkinter.X,expand=1)

Tkinter.mainloop()
