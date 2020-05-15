from tkinter import *
import time

ventana = Tk()

ventana.title("test")

image = PhotoImage(file="imagenes/tenor.gif", format="gif -index 1")

label = Label(ventana)
label.configure(image=image)
label.pack()

ventana.mainloop()