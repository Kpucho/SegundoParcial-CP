"""                         Constantes                  """
ANCHO = 800
ALTO = 704

#Colores
NEGRO=[0,0,0]
VERDE=[0,255,0]
ROJO=[255,0,0]
AMARILLO=[255,255,0]
BLANCO=[255,255,255]
AZUL=[0,0,255]
LIGHT_PINK = [212, 159, 183]


#Control
Temp0 = 10
Temp1 = 50
TamVias = 128
Vinicial = 32
Vias = []
FPS = 40

import random
import pygame

DIR = []
DIR2 = []
DIR3 = []
MUERTE = []


IMAGEN_JUGADOR =  pygame.image.load('images/sprites/cars3.png')

"""movimiento jugador"""
DIR.append(IMAGEN_JUGADOR.subsurface(0, 0, 55, 40))
DIR.append(IMAGEN_JUGADOR.subsurface(0, 40, 55, 40))
DIR2.append(IMAGEN_JUGADOR.subsurface(105, 0, 55, 40))
DIR2.append(IMAGEN_JUGADOR.subsurface(105, 40, 55, 40))
DIR3.append(IMAGEN_JUGADOR.subsurface(55, 0, 50, 40))
DIR3.append(IMAGEN_JUGADOR.subsurface(55, 40, 50, 40))

"""Jugador muere"""
MUERTE.append(IMAGEN_JUGADOR.subsurface(0, 80, 50, 40))
MUERTE.append(IMAGEN_JUGADOR.subsurface(50, 80, 50, 40))

"""Enemigos"""
ENEMIGOS = []
IMAGEN_ENEMIGOS = pygame.image.load('images/sprites/enemies.png')
ENEMIGOS.append(IMAGEN_ENEMIGOS.subsurface(0, 0, 80, 50))
ENEMIGOS.append(IMAGEN_ENEMIGOS.subsurface(0, 55, 80, 50))
ENEMIGOS.append(IMAGEN_ENEMIGOS.subsurface(0, 110, 80, 50))
ENEMIGOS.append(IMAGEN_ENEMIGOS.subsurface(0, 162, 136, 50))

"""Obstaculos"""
OBSTACULOS = []
IMAGEN_OBSTACULOS = pygame.image.load('images/sprites/obstaculos.png')
OBSTACULOS.append(IMAGEN_OBSTACULOS.subsurface(0, 530, 80, 125))




#pExito = probabilidad de conseguir cierto objetivo
def prob2(pExito):
    prob = random.randrange(100)
    if prob < pExito:
        return 1
    else:
        return 0
