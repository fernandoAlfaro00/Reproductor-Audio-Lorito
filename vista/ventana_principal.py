import os
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkFont
from mutagen import MutagenError , wave , oggvorbis
import reproductor
import pygame
import time


class VentanaPrincipal(tk.Frame):
    def __init__(self, master=None, rep=None):

        super().__init__(master)
        self.master = master
        self.configure(background="skyblue")
        self.grid(padx=8, pady=8)
        self.photoimages = {}
        self.make_components()
        self.get_styles()
        self.reproductor = rep
        self.idx_track = 0
        self.listado_pista = []
        self.nombre_pista = ""
        
    def set_titulo(self, texto: str):
        """[summary]

        Args:
            texto (str): [description]
        """
        self.nombre_pista = texto
        self.label_title.config(text=self.nombre_pista)

    def set_tiempo(self, segundo):
       
        m, s = divmod(segundo, 60)
        m, s = int(m), int(s)
        self.label_time.config(text=f"{m:02}:{s:02}")

    def set_duration(self, texto):

        self.label_duration.config(text=texto)

    def crear_menu(self):

        self.menubar = tk.Menu(self.master)
        self.opciones = tk.Menu(self.menubar, tearoff=0)
        self.master.config(menu=self.menubar)
        self.opciones.add_command(
            label="Abrir audio", command=self.open_file, accelerator="Ctrl+O"
        )
        self.menubar.add_cascade(label="Abrir", menu=self.opciones)
        self.bind_all("<Control-o>", self.key_combination)

        menu_font = ("Helvetica", 16, "bold")
        self.menubar.configure(font=menu_font)
        self.opciones.configure(font=menu_font)

    def make_components(self):

        icons_names = [
            'icon_next'
            , 'icon_previous'
            , 'icon_play'
            , 'icon_pause'
            , 'icon_stop'
            , 'icon_recover'
            , 'icon_altavoz'
            , 'icon_replay']

        files = [
            r"icons/icons8-fin-24.png"
            , r"icons/icons8-saltar-a-inicio-24.png"
            , r"icons/icons8-play-24.png"
            , r"icons/icons8-pausa-24.png"
            , r"icons/icons8-detener-24.png"
            , r"icons/icons8-lista-de-transacciones-24.png"
            , r"icons/icons8-altavoz-24.png"
            , r"icons/icons8-repetir-24.png"
        ]

        self.set_icons(icons_names, files)

        self.crear_menu()

        # Creación de frame y elemento padres(?
        self.frame_title = tk.Frame(self  )

        self.frame_title.grid( row=2 , column=0 )

        self.frame_title.configure(background="blue"  )
        self.label_title = tk.Label(
            self.frame_title, text="----" ,
            width=40
        )
        self.label_title.grid(sticky="WE")


        
        self.create_components_visual()
        self.create_components_time()
        self.create_components_control()
        self.create_components_track()
        self.create_components_volume()

        # de nuevo un after -- era para tiempo pero no se implemento
        self.after(0, self.update_time)
        # self.after(0, self.update_title)

        self.after(0, self.update_frame, 0)

        self.after(0, self.update_title, 0)

        
    def change_position(self, event):

     
        value =  float(event)
        self.reproductor.music.set_pos(value)

    def muted(self):

        
        if self.estado_volumen.get():

            imagen2 = tk.PhotoImage(file=r"icons/icons8-silencio-24.png")
            self.btn_volumen.config(image=imagen2)
            self.after_volume=  self.var_volume.get()
            self.var_volume.set(0)
            self.estado_volumen.set(False)
            self.btn_volumen.image = imagen2

        else:

            imagen1 = tk.PhotoImage(file=r"icons/icons8-altavoz-24.png")
            self.btn_volumen.config(image=imagen1)
            self.btn_volumen.image = imagen1
            self.estado_volumen.set(True)
            self.var_volume.set(self.after_volume)

        self.change_volume()

    # def recover_slice(self, event=None):      
    #     x = self.frame_volumen.winfo_x()
        
    #     self.scale_volume.place(width=20 ,y=345, x=x+10)
    #     self.label_volume.place(
    #         height=50, width=50, y=5, x=350
    #     )
       

    # def forget_slice(self, event=None):
        
    #     print(event.widget)
    #     self.scale_volume.bind('<Motion>', self.recover_slice)
    #     self.after(100,None)

    #     self.scale_volume.place_forget()
    #     self.label_volume.place_forget()
        
    def show_label_volume(self, event=None):      
      
        self.label_volume.place(
            height=50, width=50, y=5, x=350
        )
    def hide_label_volume(self,event=None):

        self.after(3000,lambda : self.label_volume.place_forget())

       



    def change_volume(self, event=None):

        value = round(self.var_volume.get(), 1)
        self.var_volume.set(value)

        self.reproductor.music.set_volume(value)
        

    def get_styles(self):

        # Estilo de los botones
        style_buttons = ttk.Style()

        style_buttons.configure(
            "W.TButton",
            background="black",
            foreground="white",
            relief="flat",
            padding=6,
            width=12,
        )
        style_buttons.map(
            "W.TButton",
            foreground=[("pressed", "yellow"), ("active", "white")],
            background=[("pressed", "!disabled", "black"),
                        ("active", "black")],
        )

        self.option_add("*TkFDialog*foreground", "darkblue")
        self.option_add("*TkChooseDir*foreground", "darkblue")
        estilo_dialog = ttk.Style(self)
        estilo_dialog.configure(".", foreground="darkblue")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=15, weight="bold")

    def set_icons(self, names: list, files: list):

        if len(names) == len(files):

            self.photoimages = dict(
                zip(names, map(lambda f: tk.PhotoImage(file=f), files)))

        else:
            raise Exception("names y files debe tener el mismo tamaño")
    
    def create_components_volume(self):

        
       
            
        self.frame_volumen = tk.Frame(self.frame_time)
        self.frame_volumen.grid(row=0, column=3)
        
        
        self.btn_volumen = tk.Button(
            self.frame_volumen, image=self.photoimages['icon_altavoz']
            , command=self.muted
            
        )
        self.btn_volumen.grid(
            row=0 , column=0
        )

        self.var_volume = tk.DoubleVar()
        self.after_volume = None

        self.label_volume = ttk.Label(self, text="--", textvariable=self.var_volume 
        , background="#75ac44" 
        ,font=("Helvetica", 30, "bold")
        ,foreground="black"
         )
        self.estado_volumen = tk.BooleanVar(value=True)

        self.var_volume.set(0.5)
        
        ttk.Style().configure('vol.Horizontal.TScale'
        , background='skyblue' , 
        troughcolor='white')
        ttk.Style().map(
            "vol.Horizontal.TScale",
            background=[
                ("pressed", "!disabled", "skyblue"),
                        ("active", "skyblue")],
            
        )
        self.scale_volume = ttk.Scale(
            self.frame_volumen,
            from_=0,
            to=1.0,
            orient=tk.HORIZONTAL,
            command=self.change_volume,
            variable=self.var_volume,
            style='vol.Horizontal.TScale'
        )
        self.scale_volume.grid(row=0 , column=1 )


        self.scale_volume.bind('<Button-1>' , self.show_label_volume)
        self.scale_volume.bind('<ButtonRelease-1>' , self.hide_label_volume)
        
        self.btn_volumen.bind('<Button-1>' , self.show_label_volume)
        self.btn_volumen.bind('<ButtonRelease-1>' , self.hide_label_volume)




        self.btn_volumen.image = self.photoimages['icon_altavoz']

    def create_components_time(self):
        self.frame_timeline = tk.Frame(self)
        self.frame_timeline.grid(row=1,column=0)
        self.var_timeline = tk.IntVar()


        self.style_scale =  ttk.Style()
        
        self.style_scale.configure('custom.Horizontal.TScale',background='magenta' ,troughcolor='white')
        self.style_scale.map(
            "custom.Horizontal.TScale",
            background=[
                ("pressed", "!disabled", "magenta"),
                        ("active", "magenta")],
            
        )
        self.progress_timeline = ttk.Scale(
            self.frame_timeline,
            from_=0,
            to=3000,
            orient=tk.HORIZONTAL,
            variable=self.var_timeline,
            length=400,
            command=self.change_position,
            style='custom.Horizontal.TScale'
        )
        self.progress_timeline.grid(row=0, column=0, sticky="WE")

    

        self.frame_time = tk.Frame(self) 
        
        self.frame_time.grid(row=3, column=0 , pady=2, sticky="NSWE" )
        self.label_time = tk.Label(self.frame_time, text="--:--" 
         )
        self.label_duration = tk.Label(self.frame_time
        , text="--:--" )

        self.label_time.grid(row=0, column=0 ,padx=(150,0) )
        tk.Label(self.frame_time, text='/').grid(row=0, column=1)
        self.label_duration.grid(row=0, column=2 , padx=(0,10) )
        
        


        
    def create_components_control(self):
        self.frame_btn = tk.Frame(self )
        self.frame_btn.grid(row=4 ,column=0 
        , sticky="WE")

        # asignar Botones a frame
        self.btn_forget = tk.Button(
            self.frame_btn,
            text="Ocultar",
            image=self.photoimages['icon_recover'],
            command=self.hide_list,
            width=100,
            compound=tk.LEFT
        )
        self.btn_Recover = tk.Button(
            self.frame_btn,
            text="Mostrar",
            image=self.photoimages['icon_recover'],
            command=self.view_list,
            width=100,
            compound=tk.LEFT
        )
        self.btn_play = tk.Button(
            self.frame_btn,
            image=self.photoimages['icon_play'],
            command=self.play,
            width=100
        )
        self.btn_next = tk.Button(
            self.frame_btn, image=self.photoimages['icon_next']
            , command=self.next_track
            , width=100
            
            
        )
        self.btn_previous = tk.Button(
            self.frame_btn, image=self.photoimages['icon_previous'], command=self.previous_track, width=100
        )
        self.btn_pause = tk.Button(
            self.frame_btn,
            image=self.photoimages['icon_pause'],
            command=self.pause,
            width=100
        )
        self.btn_stop =  tk.Button(
            self.frame_btn
            , image=self.photoimages['icon_stop']
            , command=lambda : self.reproductor.music.stop()
            , width=100
        )

        self.btn_previous.grid(row=0, column=0 ,pady=10)
        self.btn_play.grid(row=0, column=1, padx=30 , pady=10)
        self.btn_pause.grid(row=0, column=1,padx=30,pady=10)
        self.btn_next.grid(row=0, column=2 , sticky="E" ,pady=10)
        self.btn_forget.grid(row=1, column=2, pady=5)
        self.btn_stop.grid(row=1, column=1 , pady=(8,1))

        self.btn_next.image = self.photoimages['icon_next']
        self.btn_previous.image = self.photoimages['icon_previous']
        self.btn_pause.image = self.photoimages['icon_pause']
        self.btn_play.image = self.photoimages['icon_play']
        self.btn_forget.image = self.photoimages['icon_recover']

    def create_components_visual(self):
        self.label_img = tk.Label(self)

        self.label_img.grid( row=0, column=0)

        self.label_img.configure(width=400, height=400)

        self.frames = [
            tk.PhotoImage(file="imagenes/nofunciona.gif",
                          format="gif -index %i" % (i))
            for i in range(40)
        ]
    
    def view_list(self):
        self.btn_Recover.grid_remove()
        self.btn_forget.grid(row=1, column=2,pady=5)
        self.frame_track.grid()

    def hide_list(self):
        self.btn_forget.grid_remove()
        self.btn_Recover.grid(row=1, column=2,pady=5)
        self.frame_track.grid_remove()

    def create_components_track(self):

        self.frame_track = tk.Frame(self, bg="skyblue")
        self.frame_track.grid(column=1, row=0 , padx=(10,2) , rowspan=5, sticky="NSWE")

        self.checkbox_value = tk.BooleanVar(self)
    
        self.listbox = tk.Listbox(self.frame_track, 
        relief="flat"
        , height=22)
        self.scroll = tk.Scrollbar(self.frame_track, orient=tk.VERTICAL)
        self.checkbox = tk.Checkbutton(
            self.frame_track,
            command=self.auto_play,
            text="auto reproducción",
            variable=self.checkbox_value,
        )

        self.btn_replay = tk.Button(self.frame_track
        , image=self.photoimages['icon_replay'] 
        , compound=tk.LEFT
        , text="repetir listado"
        , command=self.change_state
        , activebackground='blue'
        )
        self.listbox.bind("<Double-1>", self.select_track)

        # grid
        self.listbox.grid(row=0, column=0, ipadx=5  ,  pady=(0,5)  ,  sticky="ns")

        self.scroll.grid(row=0, column=1, pady=(0,5), sticky="ns")
        # self.checkbox.grid(row=1, column=0)
        self.btn_replay.grid(row=1, column=0)
        # configure
        self.listbox.configure(width=65, selectmode=tk.SINGLE)
        self.scroll.configure(command=self.listbox.yview)



    def change_state(self):

        self.checkbox.invoke()

      
        if self.checkbox_value.get():
            print(self.btn_replay['bg'])
            self.btn_replay['bg'] = 'blue'
        else:
            self.btn_replay['bg'] = '#001621'

    def auto_play(self):
        print(self.checkbox_value.get())
        if self.checkbox_value.get():

            self.after_id = self.after(1000, self.update_autoplay)
        else:

            self.after_cancel(self.after_id)

    def update_autoplay(self):

        if not self.reproductor.music.get_busy():
            self.next_track()
        self.after(1000, self.update_autoplay)

    def update_frame(self, ind):
        frame = self.frames[ind]
        if self.reproductor.para():

            ind += 1
            # creo que era para que llegara solo 40 frame del gif
            if ind >= 40:
                ind = 0
        self.label_img.configure(image=frame, bd=0, bg="#75ac44")

        self.after(50, self.update_frame, ind)

    # actualizacion de tiempo de duración
    def update_time(self):

        if self.reproductor.music.get_busy():

            self.var_timeline.set(self.var_timeline.get()+1)
            

            self.set_tiempo(self.var_timeline.get())
            
 
            print("Tiempo var timeline ", self.var_timeline.get())
        else:

            num = 0

        self.after(1000, self.update_time)

    def update_title(self, idx):

        if self.reproductor.music.get_busy():

            if idx < len(self.nombre_pista):

                self.label_title["text"] += self.nombre_pista[idx]
                idx += 1

            else:

                idx = 0
                self.label_title["text"] += "  "

        self.after(90, self.update_title, idx)

    def open_file(self):

        open_archive = None
        try:

            filetypes = (
                ("audio files", ("*.mp3", "*.wav")),
                ("wav files", "*.wav"),
                ("all files", "*.*"),
            )
            open_archive = filedialog.askopenfilenames(
                master=self,
                initialdir=open(".my_script_lastdir").read(),
                title="Selecione un archivo",
                filetypes=filetypes,
            )
            if open_archive:

                with open(".my_script_lastdir", "w") as f:
                    f.write(os.path.split(open_archive[-1])[0])
                self.add_track(open_archive)
        except Exception as ex:
            print(ex)

    def key_combination(self, event):

        if event.keysym == "o":
            self.open_file()

    def play(self):
        self.reproductor.play_music()
        self.btn_play.grid_remove()
        self.btn_pause.grid()

    def pause(self):
        self.reproductor.pause_music()
        self.btn_pause.grid_remove()
        self.btn_play.grid()

    def next_track(self):
        if self.idx_track < self.listbox.size() - 1:
            self.listbox.selection_clear(self.idx_track)
            self.idx_track = self.idx_track + 1
            self.listbox.selection_set(self.idx_track)
            self.select_track()

    def previous_track(self):
        if self.idx_track > 0:
            self.listbox.selection_clear(self.idx_track)
            self.idx_track = self.idx_track - 1
            self.listbox.selection_set(self.idx_track)
            self.select_track()

    def add_track(self, pistas):

        self.listado_pista.extend(list(pistas))

        lista = (len(self.listado_pista) - 1) - (len(pistas) - 1)
        self.listbox.delete(0, tk.END)
        for idx, val in enumerate(self.listado_pista):
            self.listbox.insert(idx, os.path.split(val)[1])

        self.listbox.selection_set(lista)
        self.select_track()

    def select_track(self, *event):

        if len(self.listbox.curselection()) != 0:

            self.idx_track = self.listbox.curselection()[0]
            pista = self.listbox.get(self.idx_track)

            self.set_titulo(pista)
            self.reproductor.load_music(self.listado_pista[self.idx_track])
            song = ""
            songLength = "" 
            try:
                song = wave.WAVE(self.listado_pista[self.idx_track])
                songLength = song.info.length
            except MutagenError:
                print ("error")

            try:
                song = oggvorbis.OggVorbis(self.listado_pista[self.idx_track])
                songLength = song.info.length
            except MutagenError:
                print ("error")

            m, s = divmod(songLength, 60)
            m, s = int(m), int(s)
            print(songLength)
            print(f"{m:02}:{s:02}")
            self.progress_timeline["to"] = songLength
            print("Tiempo de duración", self.progress_timeline["to"])
            self.set_duration(f"{m:02}:{s:02}")
            self.var_timeline.set(0)
            self.play()
