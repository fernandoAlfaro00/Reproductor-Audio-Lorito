import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter.constants import CENTER, LEFT, OUTSIDE, RIGHT
from tkinter import BooleanVar, Frame, StringVar, filedialog, ttk
from mutagen.wave import WAVE
import reproductor


class VentanaPrincipal(tk.Frame):

    def __init__(self, master=None, rep=None):

        super().__init__(master)
        self.master = master
        self.configure(background='white')
        self.grid(padx=8, pady=8)

        self.crear_componentes()
        self.dar_estilo()
        self.reproductor = rep
        self.idx_pista = 0
        self.listado_pista = []
        self.nombre_pista = ""

    def set_titulo(self, texto):

        self.nombre_pista = texto
        self.label_titulo.config(text=self.nombre_pista)

    def set_tiempo(self, texto):

        self.label_time.config(text=texto)

    def set_duration(self, texto):

        self.label_duration.config(text=texto)

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

        menu_font = ("Helvetica", 16, "bold")
        self.menubar.configure(font=menu_font)
        self.opciones.configure(font=menu_font)

    def crear_componentes(self):

        self.crear_menu()

        # Creación de frame y elemento padres(?
        self.frame_info = tk.Frame(self)
        self.frame_btn = tk.Frame(self)
        self.frame_track = tk.Frame(self, bg="lightblue")
        self.label_img = tk.Label(self)
        self.frame_control = tk.Frame(self)
        self.frame_volumen = tk.Frame(self )
        self.frame_timeline =  tk.Frame(self)

        self.frame_volumen.place( y=325, x=371)

       

        # grid
        self.label_img.grid(column=0, row=0)
        self.frame_timeline.grid(column=0, row=1, sticky="WE")
        self.frame_control.grid(column=0, row=2, sticky="WE")
        self.frame_info.grid(column=0, row=3)
        self.frame_btn.grid(column=0, row=4)
        self.frame_track.grid(column=1, row=0, sticky='N', rowspan=3)
        # configure
        self.frame_info.configure(width=400, height=10, background="blue")
        self.frame_btn.configure(background="yellow", width=400, height=50)
        self.label_img.configure(width=400, height=400)
        

        self.label_time = tk.Label(self.frame_info, text="--:--")
        self.label_duration = tk.Label(self.frame_info, text="--:--")

        self.label_titulo = tk.Label(
            self.frame_info, justify="left", width=40,  text='----')
        self.label_titulo.grid(row=0, column=0, columnspan=3)

        self.label_time.grid(row=1, column=0)
        self.label_duration.grid(row=1, column=1)
       
        self.volumen = tk.DoubleVar()
        self.label_vol = ttk.Label(
            self, text="--", textvariable=self.volumen).place(height=50, width=50, rely=0, relx=0.38)

        self.volumen.set(0.5)
        self.scale_volumen = ttk.Scale(
            self.frame_volumen,
            from_=1.0,
            to=0,
            orient=tk.VERTICAL,
            ####################
            command=self.cambiar_volumen,
            variable=self.volumen
            
        )
        
        self.var_timeline = tk.IntVar() 
        self.progress_timeline =  ttk.Scale(
            self.frame_timeline
            ,from_=0
            ,to=3000
            ,orient=tk.HORIZONTAL
            ,variable=self.var_timeline
            ,length=400
            ,command=self.soymanco
            
        )


        

        self.progress_timeline.grid(row=0 , column=0)

        
   
        icon_altavoz = tk.PhotoImage(file=r"icons/icons8-altavoz-24.png")

        self.estado_volumen = BooleanVar(value=True)

        self.btn_volumen = tk.Button(self.frame_info, image=icon_altavoz , command=self.muted )
        


        self.frame_volumen.bindtags( self.btn_volumen.bindtags())
        self.frame_volumen.bind_class( self.btn_volumen , '<Motion>', self.recover_slice)
        self.frame_volumen.bind_class( self.btn_volumen,'<Leave>', self.forget_slice)
       
       
        self.btn_volumen.grid(row=1 , column=2 ,sticky="E" , ipadx=2, ipady=2, padx=(0,10))

        self.btn_volumen.image = icon_altavoz
        
        print(self.frame_volumen.bindtags())
        # self.progressbar = ttk.Progressbar(
        #     self.frame_control,
        #     orient=tk.HORIZONTAL,
        #     mode="indeterminate"

        # ).grid(row=0 , column=0 , sticky="EW")

        self.frame_control.grid_columnconfigure(0, weight=1)

        # imagen
        self.frames = [tk.PhotoImage(
            file='imagenes/nofunciona.gif', format='gif -index %i' % (i)) for i in range(40)]

        # de nuevo un after -- era para tiempo pero no se implemento
        self.after(0, self.update_time)
        # self.after(0, self.update_titulo)

        self.after(0, self.update_frame, 0)

        self.after(0, self.update_titulo, 0)

        self.crear_componentes_reproductor()
        self.componentes_listado_track()
    def soymanco(self , event):

        value  = int(event)
    
        
        print("Soy manco test", event)
        
    def muted(self):
        
        if self.estado_volumen.get() :

            imagen2 = tk.PhotoImage(file=r'icons/icons8-silencio-24.png')
            self.btn_volumen.config(image=imagen2)
            self.volumen.set(0)
            self.estado_volumen.set(False)
            self.btn_volumen.image = imagen2
            
        else:
            
            imagen1 = tk.PhotoImage(file=r'icons/icons8-altavoz-24.png')
            self.btn_volumen.config(image=imagen1)
            self.btn_volumen.image = imagen1
            self.estado_volumen.set(True)
            self.volumen.set(0.5)
            
        print(self.estado_volumen.get())

    def recover_slice(self, event=None):
        
        
        self.scale_volumen.pack(side='top',fill='none' )
        


    def forget_slice(self, event=None):
        self.scale_volumen.pack_forget()
       
       

   

    def cambiar_volumen(self, event):

        
        value = round(self.volumen.get(),1)
        self.volumen.set(value)

        self.reproductor.music.set_volume(value)


    def dar_estilo(self):

        # Estilo de los botones
        estilo_botones = ttk.Style()

        estilo_botones.configure("W.TButton", background='black',
                                 foreground='white', relief="flat", padding=6, width=12)
        estilo_botones.map("W.TButton",
                           foreground=[('pressed', 'yellow'),
                                       ('active', 'white')],
                           background=[('pressed', '!disabled', 'black'),
                                       ('active', 'black')]
                           )

        self.option_add('*TkFDialog*foreground', 'darkblue')
        self.option_add('*TkChooseDir*foreground', 'darkblue')
        estilo_dialog = ttk.Style(self)
        estilo_dialog.configure('.', foreground='darkblue')

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=15, weight="bold")

    def crear_componentes_reproductor(self):

        icon_next = tk.PhotoImage(file=r"icons/icons8-fin-24.png")
        icon_previous = tk.PhotoImage(
            file=r"icons/icons8-saltar-a-inicio-24.png")
        icon_play = tk.PhotoImage(file=r"icons/icons8-play-24.png")
        icon_pause = tk.PhotoImage(file=r"icons/icons8-pausa-24.png")
        icon_stop = tk.PhotoImage(file=r"icons/icons8-detener-24.png")
        icon_recover = tk.PhotoImage(
            file=r"icons/icons8-lista-de-transacciones-24.png")

        # asignar Botones a frame
        self.btn_forget = tk.Button(
            self.frame_btn, text="Ocultar", image=icon_recover, command=self.ocultar_lista, width=100, compound=LEFT)
        self.btn_Recover = tk.Button(
            self.frame_btn, text="Mostrar", image=icon_recover, command=self.mostrar_lista, width=100, compound=LEFT)
        self.btn_play = tk.Button(
            self.frame_btn, image=icon_play, command=self.play, width=100 , justify='center')
        self.btn_next = tk.Button(
            self.frame_btn, image=icon_next,   command=self.siguiente, width=100)
        self.btn_previous = tk.Button(
            self.frame_btn, image=icon_previous, command=self.anterior, width=100)
        self.btn_pause = tk.Button(
            self.frame_btn, image=icon_pause, command=self.pause, width=100 , justify='center')

        self.btn_previous.grid(row=0, column=0, sticky="W")
        self.btn_play.grid(row=0, column=1 )
        self.btn_pause.grid(row=0, column=1)
        self.btn_next.grid(row=0, column=2, sticky="E")
        self.btn_forget.grid(row=1, column=2, sticky="E")

        self.btn_next.image = icon_next
        self.btn_previous.image = icon_previous
        self.btn_pause.image = icon_pause
        self.btn_play.image = icon_play
        self.btn_forget.image = icon_recover

    def mostrar_lista(self):
        self.btn_Recover.grid_remove()
        self.btn_forget.grid(row=1, column=2, padx=(25, 0), pady=(20, 0))
        self.frame_track.grid()

    def ocultar_lista(self):
        self.btn_forget.grid_remove()
        self.btn_Recover.grid(row=1, column=2, padx=(25, 0), pady=(20, 0))
        self.frame_track.grid_remove()

    def componentes_listado_track(self):

        self.checkbox_value = tk.BooleanVar(self)
        # definición
        self.listbox = tk.Listbox(self.frame_track, relief="flat")
        self.scroll = tk.Scrollbar(self.frame_track, orient=tk.VERTICAL)
        self.checkbox = tk.Checkbutton(self.frame_track,
                                        command=self.auto_reproduccion,
                                        text="auto reproducción",
                                        variable=self.checkbox_value)
        self.listbox.bind('<Double-1>', self.seleccionar_pista)

        # grid
        self.listbox.grid(row=0, column=0, pady=5, sticky='ns')

        self.scroll.grid(row=0, column=1, pady=5, sticky="ns")
        self.checkbox.grid(row=1, column=0)
        # configure
        self.listbox.configure(width=50, selectmode=tk.SINGLE)
        self.scroll.configure(command=self.listbox.yview)

    def auto_reproduccion(self):

        if self.checkbox_value.get():

            self.after_id = self.after(1000, self.update_autoplay)
        else:

            self.after_cancel(self.after_id)

    def update_autoplay(self):

        if self.reproductor.music.get_busy() == False:
            self.siguiente()
        self.after(1000, self.update_autoplay)

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
    def update_time(self):

        if self.reproductor.music.get_busy():

            pos_time = self.reproductor.music.get_pos()

            s = pos_time // 1000
            m, s = divmod(s, 60)
            m, s = int(m), int(s)

            self.set_tiempo(f"{m:02}:{s:02}")
            self.var_timeline.set(s)

            print("Tiempo de timeline" , self.var_timeline.get())

        else:

            num = 0

        self.after(500, self.update_time)

    def update_titulo(self, idx):

        if self.reproductor.music.get_busy():

            if idx < len(self.nombre_pista):

                self.label_titulo["text"] += self.nombre_pista[idx]
                idx += 1

            else:

                idx = 0
                self.label_titulo["text"] += "  "

        self.after(90, self.update_titulo, idx)

    def abrir_archivo(self):

        archivo_abierto = None
        try:

            archivo_abierto = filedialog.askopenfilenames(master=self, initialdir=open('.my_script_lastdir').read(),
                                                          title="Selecione un archivo",

                                                          filetypes=(("audio files", ("*.mp3", "*.wav")), ("wav files", "*.wav"), ("all files", "*.*")))
            if archivo_abierto:

                with open('.my_script_lastdir', 'w') as f:
                    f.write(os.path.split(archivo_abierto[-1])[0])
                self.agregar_pista(archivo_abierto)
        except Exception as ex:
            print(ex)

    def combinacion_teclas(self, event):

        if event.keysym == "o":
            self.abrir_archivo()

    def play(self):
        self.reproductor.play_music()
        self.btn_play.grid_remove()
        self.btn_pause.grid()

    def pause(self):
        self.reproductor.pause_music()
        self.btn_pause.grid_remove()
        self.btn_play.grid()

    def siguiente(self):
        if self.idx_pista < self.listbox.size()-1:
            self.listbox.selection_clear(self.idx_pista)
            self.idx_pista = self.idx_pista + 1
            self.listbox.selection_set(self.idx_pista)
            self.seleccionar_pista()

    def anterior(self):
        if self.idx_pista > 0:
            self.listbox.selection_clear(self.idx_pista)
            self.idx_pista = self.idx_pista - 1
            self.listbox.selection_set(self.idx_pista)
            self.seleccionar_pista()

    def agregar_pista(self, pistas):

        self.listado_pista.extend(list(pistas))

        lista = (len(self.listado_pista)-1) - (len(pistas) - 1)
        self.listbox.delete(0, tk.END)
        for idx, val in enumerate(self.listado_pista):
            self.listbox.insert(idx, os.path.split(val)[1])

        self.listbox.selection_set(lista)
        self.seleccionar_pista()

    def seleccionar_pista(self, *event):

        if len(self.listbox.curselection()) != 0:

            self.idx_pista = self.listbox.curselection()[0]
            pista = self.listbox.get(self.idx_pista)

            self.set_titulo(pista)
            self.reproductor.load_music(self.listado_pista[self.idx_pista])
            song = WAVE(self.listado_pista[self.idx_pista])
            songLength = song.info.length

            m, s = divmod(songLength, 60)
            m, s = int(m), int(s)
            print(songLength)
            print(f"{m:02}:{s:02}")
            self.progress_timeline['to'] = songLength
            print("Tiempo de duración" ,  self.progress_timeline['to'])
            self.set_duration(f"{m:02}:{s:02}")
            self.play()
