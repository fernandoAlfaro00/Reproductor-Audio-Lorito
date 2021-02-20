from tkinter import *

root = Tk()

text="Lorem Ipsum"

text = (' '*20) + text + (' '*20)

marquee = Text(root, height=1, width=20)
marquee.pack()

i = 0

def command(x, i):
    marquee.insert("1.1", x)
    if i == len(text):
        i = 0
    else:
        i = i+1
    root.after(100, lambda:command(text[i:i+20], i))

button = Button(root, text="Start", command=lambda: command(text[i:i+20], i))
button.pack()

root.mainloop()