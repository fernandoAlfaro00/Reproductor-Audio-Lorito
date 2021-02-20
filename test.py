from tkinter import Frame, Tk

class MyApp():
    def __init__(self):
        self.root = Tk()

        self.my_frame_red = Frame(self.root, bg='red')
        self.my_frame_red.grid(row=0, column=0, sticky='nsew')

        self.my_frame_blue = Frame(self.root, bg='blue')
        self.my_frame_blue.configure(width="400")
        self.my_frame_blue.grid(row=0, column=1, rowspan=2, sticky='nsew')

        self.my_frame_green = Frame(self.root, bg='green')
        self.my_frame_green.grid(row=1, column=0, sticky='nsew')

        self.root.grid_rowconfigure(0, minsize=300, weight=1)
        self.root.grid_columnconfigure(0, minsize=300, weight=1)

        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, minsize=100)
        
        

        self.root.mainloop()

if __name__ == '__main__':
    app = MyApp()
