import pygame
import time

mix = pygame.mixer  # This is just me being lazy!
music = mix.music  # ditto

f1= 'C:/Codigos dos mil viente/proyectos Personales/Reproductor de audio/reproductor/error_aoe_scoutattack.wav'
f2 = 'C:/Codigos dos mil viente/proyectos Personales/Reproductor de audio/reproductor/balloon_aoe_infantryackb.wav'

track =[f1,f2]

mix.init()

def lista(track):

    for i in track:

        yield i


    
p = lista(track)
pos = pygame.mixer.music.get_pos()
if p :
    pygame.mixer.music.load(next(p))
    print(p)
 

pygame.mixer.music.play(0)
        

