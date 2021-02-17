from tkinter import filedialog, ttk
import tkinter as tk
import tkinter.font as tkFont
import os


class VentanaPrincipal(tk.Frame):

    def __init__(self, master=None , rep=None ):

        super().__init__(master)
        self.master = master
        self.configure(background='white')
        self.grid(padx=8, pady=8)


        self.crear_componentes()
        self.dar_estilo()
        self.reproductor = rep
        self.listado_pista = []


        
    def set_titulo(self, texto):

        self.label_titulo.config(text=texto)

    def crear_menu(self):

        self.menubar = tk.Menu(self.master)
        self.opciones = tk.Menu(self.menubar, tearoff=0)
        self.master.config(menu=self.menubar)
        self.opciones.add_command(label="Abrir audio",
                                  command=self.abrir_archivo,
                                  accelerator="Ctrl+O"
                                  )
        self.menubar.add_cascade(label="Abrir", menu=self.opciones)
        self.bind_all("<Control-o>", self.combinacion_teclas)
        
        menu_font = ("Helvetica",16,"bold")
        self.menubar.configure( font=menu_font)
        self.opciones.configure(font=menu_font)

        

      
      


    def crear_componentes(self):

       
        self.crear_menu()

        # Creación de frame y elemento padres(?
        self.frame_info = tk.Frame(self)
        self.frame_btn = tk.Frame(self)
        self.frame_track = tk.Frame(self, bg="lightblue")
        self.label_img = tk.Label(self)

        #grid 
        self.frame_info.grid(column=0, row=1)
        self.frame_btn.grid(column=0, row=2)
        self.frame_track.grid(column=1, row=0, sticky='NWSE')
        self.label_img.grid(column=0, row=0)

        #configure
        self.frame_info.configure(width=400, height=10, background="blue")
        self.frame_btn.configure(background="yellow", width=400, height=50)
        self.label_img.configure(width=400, height=400)
        self.frame_track.configure(bd=10)

        self.label_time = tk.Label(self.frame_info, text="0")
        self.label_titulo = tk.Label(self.frame_info, text='-----')
        self.label_titulo.grid(row=0)
        self.label_time.grid(row=1)


 



     

        # imagen
        self.frames = [tk.PhotoImage(
            file='imagenes/nofunciona.gif', format='gif -index %i' % (i)) for i in range(40)]

        # de nuevo un after -- era para tiempo pero no se implemento
        self.after(0, self.update_time, 0)
        self.after(0, self.update_frame, 0)

        self.crear_componentes_reproductor()
        self.componentes_listado_track()

    def dar_estilo(self):

         # Estilo de los botones
        estilo_botones = ttk.Style()

        estilo_botones.configure("W.TButton", background='black',
                        foreground='white', relief="flat", padding=6, width=12)
        estilo_botones.map("W.TButton",
                  foreground=[('pressed', 'yellow'), ('active', 'white')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'black')]
                  )

        self.option_add('*TkFDialog*foreground', 'darkblue')
        self.option_add('*TkChooseDir*foreground', 'darkblue')
        estilo_dialog = ttk.Style(self)
        estilo_dialog.configure('.', foreground='darkblue')

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica",size=15,weight="bold")

    def crear_componentes_reproductor(self):
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

        # definición 
        self.listbox = tk.Listbox(self.frame_track, relief="flat")
        self.scroll = tk.Scrollbar(self.frame_track, orient=tk.VERTICAL)
        self.listbox.bind('<Double-1>', self.seleccionar_pista)

        #grid
        self.listbox.grid(column=0, row=0)
        self.scroll.grid(column=1, row=0, sticky="NS")

        #configure
        self.listbox.configure(width=50, selectmode=tk.SINGLE)
        self.scroll.configure(command=self.listbox.yview)

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

    

    def abrir_archivo(self):

        # estilo para filedialog       
        archivo_abierto = None
        archivo_abierto = filedialog.askopenfilenames(master=self,
                                                      title="Selecione un archivo",
                                                      filetypes=(("audio files", ("*.mp3", "*.wav")), ("wav files", "*.wav"), ("all files", "*.*")))

        self.listado_pista.extend(list(archivo_abierto))

        self.agregar_pista()

    def combinacion_teclas(self, event):

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

    def agregar_pista(self):
        self.listbox.delete(0, tk.END)
        for idx, val in enumerate(self.listado_pista):
            self.listbox.insert(idx, os.path.split(val)[1])

    def seleccionar_pista(self, event):

        if len(self.listbox.curselection()) != 0:

            idx_seleccionado = self.listbox.curselection()[0]
            pista = self.listbox.get(idx_seleccionado)
            print(pista)
            self.set_titulo(pista)
            