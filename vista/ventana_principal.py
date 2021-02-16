from tkinter import filedialog, ttk
import tkinter as tk
import os
from reproductor.audio import Reproductor


class VentanaPrincipal(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.crear_componentes()
        self.reproductor = Reproductor()

     # TODO:mejorar implementación de los grid
    def crear_componentes(self):

        #barra superior (menu)
        self.crear_menu()

        #Creación de frame
        #frame principal
        self.configure(background='white')
        self.grid(padx=8, pady=8)
        self.bind_all("<Control-o>", self.cambiar)
        #Frame de imagen lorito
        self.label_img = tk.Label(self)
        self.label_img.grid(column=0, row=0 )
        self.label_img.configure(width=400 , height=400)

        #Frame titulo y tiempo
        self.frame_info = tk.Frame(self)
        self.frame_info.grid(column=0, row = 1 )
        self.frame_info.configure(width=400 , height= 10  , background="blue" )

        # Frame de botones
        self.frame_btn = tk.Frame(self)
        self.frame_btn.configure(background="yellow")
        self.frame_btn.grid(column=0, row=2)
        self.frame_btn.configure(width=400 , height=50)

        #Frame de listado de pistas
        self.frame_track = tk.Frame(self, bg="lightblue")
        self.frame_track.config(bd=10 )
        self.frame_track.grid(column=1, row=0, sticky ='NWSE'  )



        # Titulo de la pista
        self.label_titulo = tk.Label(self.frame_info, text='-----')
        self.label_titulo.grid( row=0)

        # Tiempo de duracion de la pista
        self.label_time = tk.Label(self.frame_info, text="0")
        self.label_time.grid( row=1)
   

        self.crear_componentes_reproductor()
        # imagen
        self.frames = [tk.PhotoImage(
            file='imagenes/nofunciona.gif', format='gif -index %i' % (i)) for i in range(40)]

        # de nuevo un after -- era para tiempo pero no se implemento
        self.after(0, self.update_time, 0)
        self.after(0, self.update_frame, 0)

        self.componentes_listado_track()


    def crear_menu(self):

        # Menu
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.opciones = tk.Menu(self.menubar, tearoff=0)
        self.opciones.add_command(label="Abrir audio",
                                  command=self.abrir_archivo,
                                  accelerator="Ctrl+O"
                                  )
        self.menubar.add_cascade(label="Abrir", menu=self.opciones)

    def crear_componentes_reproductor(self):



        #Estilo de los botones
        style = ttk.Style()


        style.configure("W.TButton", background='black',
                        foreground='white', relief="flat", padding=6, width=12)
        style.map("W.TButton",
                  foreground=[('pressed', 'yellow'), ('active', 'white')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'black')]
                  )
        
        # asignar Botones a frame
        self.btn_forget = tk.Button(
            self.frame_btn, text="Ocultar", command=self.ocultar_lista)
        self.btn_Recover = tk.Button(
            self.frame_btn, text="Mostrar", command=self.mostrar_lista)
        self.btn_play = ttk.Button(
            self.frame_btn, text="Play", command=self.play, style='W.TButton')
        self.btn_next = ttk.Button(
            self.frame_btn, text="Siguiente", command=self.siguiente, style='W.TButton')
        self.btn_previous = ttk.Button(
            self.frame_btn, text="Anterior", command=self.anterior, style='W.TButton')
        self.btn_pause = ttk.Button(
            self.frame_btn, text="Pause", command=self.Pause, style='W.TButton')


        self.btn_play.grid(column=2, row=2)
        self.btn_next.grid(column=3, row=2)
        self.btn_previous.grid(column=1, row=2)
        self.btn_pause.grid(column=2, row=3)
        self.btn_forget.grid(column=3, row=3)


    def mostrar_lista(self):
        self.btn_Recover.grid_remove()
        self.btn_forget.grid(column=3, row=3)
        self.frame_track.grid()
        
    
    def ocultar_lista(self):
        self.btn_forget.grid_remove()
        self.btn_Recover.grid(column=3, row=3)
        self.frame_track.grid_remove()
        

        

    def componentes_listado_track(self):

        # TODO:Ver para que servia esta linea -- creo que era para actualizar la ventana con el objecivo de mover al lorito.

        
       
        # listado para las pistas
        self.listbox = tk.Listbox(self.frame_track, relief="flat")
        self.listbox.bind('<<ListboxSelect>>', self.recuperar)
        self.listbox.configure( width=50)
        self.listbox.grid(column=0, row=0 )

        # parte de scroll
        self.scroll = tk.Scrollbar(self.frame_track, orient=tk.VERTICAL)
        self.scroll.configure(command=self.listbox.yview)
        self.scroll.grid(column=1, row=0  , sticky="NS")
        

    def update_frame(self, ind):
        frame = self.frames[ind]
        if self.reproductor.para():

            ind += 1
            # creo que era para que llegara solo 40 frame del gif
            if ind >= 40:
                ind = 0
        self.label_img.configure(image=frame, bd=0, bg='#75ac44')

        self.after(50, self.update_frame, ind)

    # actualizacion de tiempo de duración
    def update_time(self, num):

        if self.reproductor.para():

            num += 1
            print("tiempo: ", num)
        else:

            num = 0

        self.after(1000, self.update_time, num)

    # TODO:Mejorar este metodo
    def abrir_archivo(self):

        ruta_prueba = os.getcwd()
        archivo_abierto = filedialog.askopenfilenames(initialdir=ruta_prueba,
        title="Selecione un archivo", 
        filetypes=(("audio files", ("*.mp3", "*.wav")), ("wav files", "*.wav"), ("all files", "*.*")))

        self.reproductor.stop_music()
        self.reproductor.add_track(archivo_abierto)
        pista = self.reproductor.llamar_pista(self.reproductor.posicion_lista)
        self.reproductor.load_music(pista)
        self.label_titulo.config(text=self.reproductor.get_titulo())

        print("Titulo de la pista", self.reproductor.get_titulo())
        self.list_track()

    def cambiar(self, event):

        if event.keysym == "o":
            self.abrir_archivo()

    def play(self):
        self.reproductor.play_music()

    def siguiente(self):
        self.reproductor.siguiente()
        self.label_titulo.config(text=self.reproductor.get_titulo())

    def anterior(self):
        self.reproductor.anterior()
        self.label_titulo.config(text=self.reproductor.get_titulo())

    def Pause(self):
        self.reproductor.pause_music()

    def mostrar_nombre(self):
        pass

    def list_track(self):

        n = 1
        # self.listbox = tk.Listbox(self.frame_track, relief="flat")
        # self.listbox.bind('<<ListboxSelect>>', self.recuperar)

        # self.listbox.grid(column=1, row=0)
        for i in self.reproductor.list_track:
            n = n + 1
            self.listbox.insert(n, os.path.split(i)[1])

    def recuperar(self, event):

        if len(self.listbox.curselection()) != 0:
           # self.label_titulo.configure(text=self.listbox.get(self.listbox.curselection()[0]))
            numero = self.listbox.curselection()[0]
            print("numero pista", numero)
            pista = self.reproductor.llamar_pista(numero)
            print("nombre la pista", pista)
            self.reproductor.load_music(pista)
            self.label_titulo.config(text=self.reproductor.get_titulo())
