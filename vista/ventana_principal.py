from tkinter import filedialog
from tkinter import *
from reproductor.audio import Reproductor
import os

class VentanaPrincipal:

    def __init__(self):
        
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.bind_all("<Control-o>", self.cambiar)        
        self.inicilizar_componentes()
         
        self.reproductor = Reproductor()
       
        self.ventana.mainloop()

     


    #TODO:mejorar implementación de los grid
    def inicilizar_componentes(self):

        #Menu 
        self.menubar = Menu(self.ventana)
        self.ventana.config(menu=self.menubar)
        self.opciones = Menu(self.menubar, tearoff=0)
        self.opciones.add_command(label="Abrir audio",
                                  command=self.abrir_archivo,
                                  accelerator="Ctrl+O"
                                  )
        self.menubar.add_cascade(label="Abrir", menu=self.opciones)
        
        

        #inicialización de botones
        self.btn_play = Button(text="Play", command=self.play) 
        self.btn_next = Button(text="Siguiente", command=self.siguiente)
        self.btn_previous = Button(text="Anterior", command=self.anterior)
        self.btn_pause = Button(text="Pause", command=self.Pause)

        self.btn_play.grid(column=2, row=2)
        self.btn_next.grid(column=3, row=2)
        self.btn_previous.grid(column=1, row=2)
        self.btn_pause.grid(column=2, row=3)
        

        #label? tal vez del titulo
        self.label = Label(self.ventana, text='')
        self.label.grid(column=1, row=1, columnspan=3)
    

        self.frames = [PhotoImage(
            file='imagenes/nofunciona.gif', format='gif -index %i' % (i)) for i in range(40)]
        self.label_img = Label(self.ventana)

        self.label_img.grid(column=1, row=0, columnspan=3)
        self.label_time = Label(self.ventana, text="0")
        self.label_time.grid(column=1, row=4, columnspan=3)
        #TODO:Ver para que servia esta linea -- creo que era para actualizar la ventana con el objecivo de mover al lorito.
        
        self.ventana.after(0, self.update, 0)
        self.frame = Frame(bg="lightblue")
        self.frame.config(bd=20)
        self.frame.grid(column=6, row=0)

        #Inicializacion listado para las pistas
        self.listbox = Listbox(self.frame, relief="flat")
        self.listbox.bind('<<ListboxSelect>>', self.recuperar)
        self.listbox.grid(column=6, row=0)

        # de nuevo un after -- era para tiempo pero no se implemento
        self.ventana.after(0, self.update_time, 0)

        #parte de scroll
        self.scroll = Scrollbar(self.ventana, orient=VERTICAL)
        self.scroll.configure(command=self.listbox.yview)
        self.scroll.grid(column=7, row=0, sticky='NS')


    def update(self, ind):
        frame = self.frames[ind]
        if self.reproductor.para():

            ind += 1
            #creo que era para que llegara solo 40 frame del gif
            if ind >= 40:
                ind = 0
        self.label_img.configure(image=frame, bd=0, bg='#75ac44')

        self.ventana.after(50, self.update, ind)

    #actualizacion de tiempo de duración 
    def update_time(self, num):

        if self.reproductor.para():

            num += 1
            print("tiempo: ", num)
        else:

            num = 0

        self.ventana.after(1000, self.update_time, num)

    #TODO:Mejorar este metodo
    def abrir_archivo(self):

        ruta_prueba = os.getcwd()
        archivo_abierto = filedialog.askopenfilenames(initialdir=ruta_prueba,

                                                      title="Selecione un archivo", filetypes=(("audio files", ("*.mp3", "*.wav")), ("wav files", "*.wav"), ("all files", "*.*")))
                                                      
        self.reproductor.stop_music()
        self.reproductor.add_track(archivo_abierto)
        pista = self.reproductor.llamar_pista(self.reproductor.posicion_lista)
        self.reproductor.load_music(pista)
        self.label.config(text=self.reproductor.get_titulo())

        print("Titulo de la pista",self.reproductor.get_titulo())
        self.list_track()

    def cambiar(self, event):

        if event.keysym == "o":
            self.abrir_archivo()

    def play(self):
        self.reproductor.play_music()

    def siguiente(self):
        self.reproductor.siguiente()
        self.label.config(text=self.reproductor.get_titulo())

    def anterior(self):
        self.reproductor.anterior()
        self.label.config(text=self.reproductor.get_titulo())

    def Pause(self):
        self.reproductor.pause_music()

    def mostrar_nombre(self):
        pass

    def list_track(self):

        n = 1
        self.listbox = Listbox(self.frame, relief="flat")
        self.listbox.bind('<<ListboxSelect>>', self.recuperar)

        self.listbox.grid(column=6, row=0)
        for i in self.reproductor.list_track:
            n = n + 1
            self.listbox.insert(n, os.path.split(i)[1])

    def recuperar(self, event):

        if len(self.listbox.curselection()) != 0:
           # self.label.configure(text=self.listbox.get(self.listbox.curselection()[0]))
            numero = self.listbox.curselection()[0]
            print("numero pista", numero)
            pista = self.reproductor.llamar_pista(numero)
            print("nombre la pista", pista)
            self.reproductor.load_music(pista)
            self.label.config(text=self.reproductor.get_titulo())
