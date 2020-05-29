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
LIGHT_PINK = [212, 159, 183]

#Temporizadores de modificadores
Tx2 = 20
Tinmu = 10
Tviva = 25
Tlenti = 20

#Control
Temp0 = 40
Temp1 = 80
TamVias = 128
Vinicial = 32
carretera = [1,2,3]
Vias = []
FPS = 40

import random

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
    prob = random.randrange(121)
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
    else:
        return -1
