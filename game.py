import pygame
from config import *

if __name__ == '__main__':

    pygame.init()
    ventana = pygame.display.set_mode([ANCHO,ALTO])

    fin = False

    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
