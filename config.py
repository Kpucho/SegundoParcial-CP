"""                         Constantes                  """
ANCHO = 800
ALTO = 704

#Colores
NEGRO=[0,0,0]
VERDE=[0,255,0]
ROJO=[255,0,0]
AMARILLO=[255,255,0]
DORADO = [212, 175, 55]
BLANCO=[255,255,255]
AZUL=[0,0,255]
LIGHT_ROJO = [255,55,55]
LIGHT_PINK = [212, 159, 183]

#Temporizadores de modificadores
Tx2 = 100
Tinmu = 60
Tviva = 80
Tlenti = 80

#Control
Temp0 = 40
Temp1 = 80
TamVias = 128
Vinicial = 32
carretera = [1,2,3]
Vias = []
FPS = 40
Puntaje = 0

import random
import pygame

DIR = []
DIR2 = []
DIR3 = []
MUERTE = []

INMU = []
INMU1 = []
INMU2 = []

IMAGEN_JUGADOR_HORIZONTAL =  pygame.image.load('images/sprites/car0.png')
IMAGEN_JUGADOR_ABAJO =  pygame.image.load('images/sprites/car2.png')
IMAGEN_JUGADOR_ARRIBA =  pygame.image.load('images/sprites/car1.png')

INMUCAR_HORIZONTAL = pygame.image.load('images/sprites/inmucar0.png')
INMUCAR_VERTICAL = pygame.image.load('images/sprites/inmucar1.png')
INMUCAR_ABAJO = pygame.image.load('images/sprites/inmucar2.png')


"""movimiento jugador"""

"""horizontal"""
for c in range(4):
    DIR.append(IMAGEN_JUGADOR_HORIZONTAL.subsurface(60*c, 0, 60, 40))

for c in range(4):
    DIR2.append(IMAGEN_JUGADOR_ABAJO.subsurface(60*c, 0, 60, 47))

for c in range(4):
    DIR3.append(IMAGEN_JUGADOR_ARRIBA.subsurface(60*c, 0, 60, 47))


"""inmune """
for c in range(4):
    INMU.append(INMUCAR_HORIZONTAL.subsurface(60*c, 0, 60, 40))

for c in range(4):
    INMU1.append(INMUCAR_VERTICAL.subsurface(60*c, 0, 60, 47))

for c in range(4):
    INMU2.append(INMUCAR_ABAJO.subsurface(60*c, 0, 60, 47))

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
OBSTACULOS.append(IMAGEN_OBSTACULOS.subsurface(131, 287, 50, 62))

"""Modificadores"""
im_modificadores = pygame.image.load('images/sprites/modificadores.png')
MODIFI = []
for c in range(5):
    cuadro=im_modificadores.subsurface(64*c,0,64,64)
    MODIFI.append(cuadro)

#pExito = probabilidad de conseguir cierto objetivo
def prob2(pExito):
    prob = random.randrange(101)
    if prob < pExito:
        return 1
    else:
        return 0

#pExito = probabilidad de conseguir cierto objetivo
def prob3(pExito):
    prob = random.randrange(101)
    if prob < pExito/3:
        return 1
    elif prob < 2*pExito/3:
        return 2
    else:
        return 3

#pExito = probabilidad de conseguir cierto objetivo
def prob5(pExito):
    prob = random.randrange(pExito)
    if prob < pExito/5:
        return 4
    elif prob < 2*pExito/5:
        return 3
    elif prob < 3*pExito/5:
        return 2
    elif prob < 4*pExito/5:
        return 1
    elif prob < pExito:
        return 0
