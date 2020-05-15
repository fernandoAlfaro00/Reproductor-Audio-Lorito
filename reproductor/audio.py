import pygame
import os 

class Reproductor():
    
    
    
    def __init__(self):
        self.mix = pygame.mixer  
        self.music = self.mix.music
        
        self.mix.init()
        self.pause = False
        self.music_pause = "audio_reproductor/mario_bros_paused.wav"
        self.sound = self.mix.Sound(self.music_pause)
        self.nombre_archivo = ''

        
        

        self.list_track = []
       
        self.posicion_lista = 0 
        self.p = self.lista(self.list_track)
        
        

        
    def load_music(self,track):
        self.music.load(track)
        self.set_titulo(track)

        
        

    def play_music(self):

        if self.pause == True:
            self.music.unpause()
            self.sound.stop()
            return

        self.music.play()
        

    def  pause_music(self):

        self.music.pause()
        self.pause =  not self.pause
        print(self.pause)
        self.sound.play()
        
        

    def  mostrar_tiempo(self):

    
        return  self.music.get_pos()

    def  para(self):

        if self.music.get_busy() :
            
            return  True

        return False


    def stop_music(self):

        self.music.stop()
    
    def get_titulo(self):
        
        return self.nombre_archivo

    def set_titulo(self, track):

        self.nombre_archivo = os.path.split(track)[1]

    def lista(self,track):

            for i in track:

                yield i


    def lista_rev(self,track):

            for i in reversed(track[:-1]):

                yield i

    def add_track(self,*track):
        for i in track:
            for t in i :

                self.list_track.append(t)

    def tracks(self):


            return self.list_track


    def  llamar_pista(self , posicion):
        n = 0
        for i in self.list_track:

            if n== posicion :

                return  i
            n = n+ 1
        
        return ""


    def siguiente(self):
        
        if self.posicion_lista < len(self.list_track)-1:
            self.posicion_lista =  self.posicion_lista + 1
            pista = self.llamar_pista(self.posicion_lista)
            self.load_music(pista)
            

            
            

        
    def anterior(self):
        
        if self.posicion_lista > 0 :
            self.posicion_lista =  self.posicion_lista - 1
            pista = self.llamar_pista(self.posicion_lista)
            self.load_music(pista)
            
           


        
    







